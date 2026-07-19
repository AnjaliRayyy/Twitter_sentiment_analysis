from __future__ import annotations

import io
import unittest

from xquik_import import XquikImportError, load_xquik_texts


class NamedUpload(io.BytesIO):
    def __init__(self, name: str, content: str | bytes) -> None:
        super().__init__(content.encode() if isinstance(content, str) else content)
        self.name = name

    def getvalue(self) -> bytes:
        return super().getvalue()


class XquikImportTests(unittest.TestCase):
    def test_reads_csv_text_fields(self) -> None:
        self.assertEqual(
            load_xquik_texts(NamedUpload("tweets.csv", "id,full_text\n1,Great update\n")),
            ["Great update"],
        )

    def test_reads_json_nested_tweet_text(self) -> None:
        upload = NamedUpload("tweets.json", '{"data":[{"tweet":{"text":"Nested tweet"}}]}')

        self.assertEqual(load_xquik_texts(upload), ["Nested tweet"])

    def test_reads_nested_api_response(self) -> None:
        upload = NamedUpload(
            "tweets.json",
            '{"data":{"tweets":[{"text":"Nested response"}]}}',
        )

        self.assertEqual(load_xquik_texts(upload), ["Nested response"])

    def test_reads_jsonl_rows(self) -> None:
        upload = NamedUpload("tweets.jsonl", '{"text":"First"}\n{"content":"Second"}\n')

        self.assertEqual(load_xquik_texts(upload), ["First", "Second"])

    def test_rejects_missing_text(self) -> None:
        with self.assertRaises(XquikImportError):
            load_xquik_texts(NamedUpload("tweets.json", '{"data":[{"id":"1"}]}'))

    def test_rejects_invalid_json_with_import_error(self) -> None:
        with self.assertRaisesRegex(XquikImportError, "invalid structured data"):
            load_xquik_texts(NamedUpload("tweets.json", '{"tweets":['))

    def test_rejects_non_utf8_upload_with_import_error(self) -> None:
        with self.assertRaisesRegex(XquikImportError, "UTF-8"):
            load_xquik_texts(NamedUpload("tweets.csv", b"text\n\xff\n"))


if __name__ == "__main__":
    unittest.main()
