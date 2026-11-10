from __future__ import annotations

from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from tools._shared import err


def _source_key(url: str) -> str:
    """Build a comparison key without changing the URL returned to the user."""
    url = url.strip()
    if any(character.isspace() or ord(character) < 32 or ord(character) == 127 for character in url):
        raise ValueError("url must not contain whitespace or control characters")
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("url must be an absolute HTTP(S) URL")

    # urlsplit validates IPv6 syntax; accessing port validates its type/range.
    port = parsed.port
    host = parsed.hostname.lower()
    authority = f"[{host}]" if ":" in host else host
    if port is not None and port != {"http": 80, "https": 443}[parsed.scheme]:
        authority += f":{port}"
    if "@" in parsed.netloc:
        # User information is case-sensitive even though hostnames are not.
        authority = parsed.netloc.rsplit("@", 1)[0] + "@" + authority

    query = [(key, value) for key, value in parse_qsl(parsed.query, keep_blank_values=True)
             if not key.lower().startswith("utm_") and key.lower() not in {"fbclid", "gclid"}]
    # Sort distinct parameter names, preserving the order of repeated values:
    # ?tag=a&tag=b can describe a different resource from ?tag=b&tag=a.
    query.sort(key=lambda pair: pair[0])
    return urlunsplit((parsed.scheme, authority, parsed.path or "/", urlencode(query), ""))


def deduplicate_sources(items: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Remove repeat HTTP(S) sources, preserving first item and input order.

    Compare canonical URLs while retaining original item fields and URLs. Items
    with no URL remain separate. Invalid input returns an error dict with no
    partial success result. This function does not call the network or mutate
    its inputs; runtime is O(n) apart from sorting each URL's query parameters.
    """
    try:
        if items is None:
            items = []
        if not isinstance(items, list):
            raise ValueError("items must be a list of objects")
        kept: list[dict[str, Any]] = []
        seen: set[str] = set()
        for item in items:
            if not isinstance(item, dict):
                raise ValueError("each item must be an object")
            url = item.get("url")
            if url is None or url == "":
                kept.append(dict(item))
                continue
            if not isinstance(url, str):
                raise ValueError("url must be a string")
            identity = _source_key(url)
            if identity not in seen:
                seen.add(identity)
                kept.append(dict(item))
        return {"tool": "deduplicate", "items": kept,
                "input_count": len(items), "duplicates_removed": len(items) - len(kept)}
    except Exception as exc:
        return err("deduplicate", exc)
