---
name: deduplicate
track: core
kind: local_formatter
provider: local
requires_env: []
inputs: [items]
outputs: [items, input_count, duplicates_removed]
side_effect: false
requires_confirmation: false
---

# deduplicate — Tool V2

Remove repeated source URLs from items supplied by the user or retrieved by
another research tool, before formatting a digest. The registered agent name is
`deduplicate`; the Python implementation is `deduplicate_sources`.

## When to use

Use when the user requests duplicate-source removal and actual items are
available. It does not search, fetch, summarize, or decide whether different
URLs contain equivalent text. Ask `clarify` when the source items are missing.
Then pass the returned `items` to `format` if a digest was requested.

## Input

`items`: list of objects, required in the agent declaration. Each object can
contain `url`, `title`, `summary`, `source`, `section`, or additional metadata.
When present, `url` must be an absolute HTTP(S) string without internal whitespace
or control characters. Items with a missing, null, or empty URL stay separate;
matching titles alone do not prove duplicate sources. Calling the Python
function with `None` or an empty list returns an empty success result.

## Comparison rules

- Keep the first item for each canonical URL and retain original item order.
- Preserve the original URL and all metadata in the output; do not mutate input.
- Compare hostnames without case; treat HTTP port 80 and HTTPS port 443 as defaults.
- An empty path matches `/`. Remove fragments and tracking parameters `utm_*`,
  `fbclid`, and `gclid` (parameter-name comparison is case-insensitive).
- Sort distinct query parameter names; retain blank values and repeated-value
  order. Preserve meaningful query parameters, scheme, path case, user-info case,
  non-default ports, trailing slashes, and the distinction between `www` and bare
  hostnames. This avoids merging different resources without fetching them.

## Output

Success returns an object with `tool="deduplicate"`, `items`, `input_count`, and
`duplicates_removed`. Invalid list/item/URL types, malformed URLs, and invalid
ports return `{ "tool": "deduplicate", "error": "ValueError", "message": "..." }`
without raising an exception or returning partial results.

Example input:

```json
{"items":[{"title":"First","url":"https://example.com/a?utm_source=x"},{"title":"Again","url":"https://EXAMPLE.com:443/a#intro"}]}
```

Example output:

```json
{"tool":"deduplicate","items":[{"title":"First","url":"https://example.com/a?utm_source=x"}],"input_count":2,"duplicates_removed":1}
```

No key, network call, file write, or confirmation is required. Comparison uses
O(n) storage/time apart from sorting query parameters within each URL.

## Verification

Run from `starter_v0/`:

```text
python -m pytest tests/test_tools_todo.py -k deduplicate
python -m pytest tests/test_deduplicate.py tests/test_tool_contract.py
```

The dedicated tests exercise real agent dispatch with an explicitly fake model
provider and no network. The two `TOOLV2_DEDUP_*` cases in `data/eval_group.json`
measure model routing. Their expected arguments intentionally omit object lists
because the starter evaluator cannot sort dictionaries; exact item forwarding
is covered by the agent integration test. These eval cases can be run with the
team's chosen prompt/model; adding them does not assert a live-model score.
