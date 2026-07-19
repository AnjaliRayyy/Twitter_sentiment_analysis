"""Helpers for reading tweet text from Xquik export files."""

from __future__ import annotations

import csv
import io
import json
from collections.abc import Iterable
from typing import Any


TEXT_FIELDS = (
    "text",
    "full_text",
    "tweet_text",
    "content",
    "body",
    "caption",
    "message",
)
CONTAINER_FIELDS = ("data", "items", "results", "tweets", "posts")


class XquikImportError(ValueError):
    """Raised when an uploaded export cannot provide tweet text."""


def load_xquik_texts(uploaded_file: Any) -> list[str]:
    """Return cleaned tweet text values from a CSV, JSON, or JSONL upload."""

    file_name = str(getattr(uploaded_file, "name", "")).lower()
    raw_content = uploaded_file.getvalue()
    try:
        content = (
            raw_content.decode("utf-8-sig")
            if isinstance(raw_content, bytes)
            else str(raw_content)
        )
        if file_name.endswith(".csv"):
            texts = _texts_from_csv(content)
        elif file_name.endswith((".jsonl", ".ndjson")):
            texts = _texts_from_jsonl(content)
        else:
            texts = _texts_from_json(json.loads(content))
    except UnicodeDecodeError as error:
        raise XquikImportError("Export files must use UTF-8 encoding.") from error
    except (csv.Error, json.JSONDecodeError) as error:
        raise XquikImportError("The export contains invalid structured data.") from error

    cleaned = [text.strip() for text in texts if text.strip()]
    if not cleaned:
        raise XquikImportError("No tweet text fields were found in this export.")
    return cleaned


def _texts_from_csv(content: str) -> list[str]:
    reader = csv.DictReader(io.StringIO(content))
    if reader.fieldnames is None:
        raise XquikImportError("CSV exports need a header row.")
    return [_extract_text(row) for row in reader]


def _texts_from_json(content: Any) -> list[str]:
    if isinstance(content, list):
        return [_extract_text(item) for item in content]
    if isinstance(content, dict):
        for field_name in CONTAINER_FIELDS:
            nested = content.get(field_name)
            if isinstance(nested, (dict, list)):
                return _texts_from_json(nested)
        return [_extract_text(content)]
    raise XquikImportError("JSON exports must contain an object or a list.")


def _texts_from_jsonl(content: str) -> list[str]:
    rows = [line for line in content.splitlines() if line.strip()]
    return [_extract_text(json.loads(row)) for row in rows]


def _extract_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if not isinstance(value, dict):
        return ""

    for field_name in TEXT_FIELDS:
        field_value = value.get(field_name)
        if isinstance(field_value, str):
            return field_value

    for nested_field in ("tweet", "post"):
        nested = value.get(nested_field)
        if isinstance(nested, dict):
            text = _extract_text(nested)
            if text:
                return text

    return _first_nested_text(value.values())


def _first_nested_text(values: Iterable[Any]) -> str:
    for value in values:
        if isinstance(value, dict):
            text = _extract_text(value)
            if text:
                return text
    return ""
