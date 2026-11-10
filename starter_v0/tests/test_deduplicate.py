"""Offline Tool V2 tests for source identity, validation and real agent dispatch."""
from copy import deepcopy
from pathlib import Path

import pytest

from agent import ResearchAgent
from providers.base import ModelResponse, ToolCall
from tools import TOOL_FUNCTIONS, load_tool_declarations, to_openai_tools

deduplicate = TOOL_FUNCTIONS["deduplicate"]


@pytest.mark.parametrize("items", [None, []])
def test_empty_input_is_a_success(items):
    assert deduplicate(items) == {"tool": "deduplicate", "items": [],
                                  "input_count": 0, "duplicates_removed": 0}


@pytest.mark.parametrize("first,second", [
    ("https://EXAMPLE.com/a", "https://example.com/a"),
    ("https://example.com", "https://example.com/"),
    ("http://example.com:80/a", "http://example.com/a"),
    ("https://example.com:443/a", "https://example.com/a"),
    ("https://example.com/a?UTM_Source=x&fbclid=y&gclid=z", "https://example.com/a#intro"),
    ("https://example.com/a?b=2&a=1", "https://example.com/a?a=1&b=2"),
    ("https://[2001:db8::1]:443/a", "https://[2001:db8::1]/a"),
    ("  https://example.com/a  ", "https://example.com/a"),
])
def test_equivalent_source_urls_keep_the_first_original_item(first, second):
    original = {"url": first, "title": "First", "metrics": {"views": 3}}
    result = deduplicate([original, {"url": second, "title": "Duplicate"}])
    assert result["items"] == [original]
    assert result["items"][0]["url"] == first
    assert result["input_count"] == 2 and result["duplicates_removed"] == 1


@pytest.mark.parametrize("first,second", [
    ("http://example.com/a", "https://example.com/a"),
    ("https://www.example.com/a", "https://example.com/a"),
    ("https://example.com/A", "https://example.com/a"),
    ("https://example.com/a/", "https://example.com/a"),
    ("https://example.com:8443/a", "https://example.com/a"),
    ("https://example.com/a?id=1", "https://example.com/a?id=2"),
    ("https://example.com/a?filter=", "https://example.com/a"),
    ("https://example.com/a?tag=a&tag=b", "https://example.com/a?tag=b&tag=a"),
    ("https://User@example.com/a", "https://user@example.com/a"),
])
def test_distinct_resources_are_not_merged(first, second):
    items = [{"url": first}, {"url": second}]
    result = deduplicate(items)
    assert result["items"] == items
    assert result["duplicates_removed"] == 0


def test_missing_urls_are_not_deduplicated_by_title():
    items = [{"title": "Same"}, {"title": "Same", "url": ""}, {"title": "Same", "url": None}]
    assert deduplicate(items)["items"] == items


def test_original_items_order_and_nested_metadata_are_unchanged():
    items = [{"url": "https://example.com/b", "metadata": {"tags": ["research"]}},
             {"url": "https://example.com/a"}, {"url": "https://example.com/b#duplicate"}]
    before = deepcopy(items)
    result = deduplicate(items)
    assert items == before
    assert result["items"] == before[:2]
    assert result["items"][0] is not items[0]
    assert deduplicate(result["items"])["items"] == result["items"]


@pytest.mark.parametrize("items", ["", {}, 42, False, [None], ["not an object"]])
def test_invalid_container_or_item_returns_error_without_partial_success(items):
    result = deduplicate(items)
    assert result["error"] == "ValueError"
    assert result["tool"] == "deduplicate"
    assert "items" not in result


@pytest.mark.parametrize("url", [
    123, False, " ", "ftp://example.com/a", "/article", "https://",
    "https://example.com:bad/a", "https://example.com:99999/a", "https://[broken",
    "https://exa mple.com/a", "https://example.com/a\nb",
])
def test_invalid_url_returns_error_even_after_a_valid_item(url):
    result = deduplicate([{"url": "https://example.com/valid"}, {"url": url}])
    assert result["error"] == "ValueError"
    assert "items" not in result


def test_agent_sees_declared_tool_and_dispatches_original_items():
    items = [{"title": "First", "url": "https://example.com/a"},
             {"title": "Again", "url": "https://example.com/a?utm_source=mail"}]
    declarations = load_tool_declarations(Path(__file__).resolve().parents[1] / "artifacts/tools.yaml")
    schemas = to_openai_tools(declarations)

    class FakeModelProvider:
        def complete(self, messages, tools=None, **kwargs):
            assert tools == schemas
            schema = next(t["function"] for t in tools if t["function"]["name"] == "deduplicate")
            assert schema["parameters"]["required"] == ["items"]
            return ModelResponse(tool_calls=[ToolCall("deduplicate", {"items": items})])

    run = ResearchAgent(FakeModelProvider(), system_prompt="test", tools=schemas).run(
        [{"role": "user", "content": "Remove duplicate sources before making a digest."}])
    assert len(run.tool_results) == 1
    assert run.tool_results[0]["tool"] == "deduplicate"
    assert run.tool_results[0]["args"] == {"items": items}
    assert run.tool_results[0]["result"] == {"tool": "deduplicate", "items": [items[0]],
                                             "input_count": 2, "duplicates_removed": 1}
