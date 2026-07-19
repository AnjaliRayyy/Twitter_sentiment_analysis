import unittest

from preprocessor import clean_text


class CleanTextTests(unittest.TestCase):
    def test_normalizes_whitespace_left_by_removed_content(self) -> None:
        text = "  Visit https://example.com @User #Great!!!  Day 2 "

        self.assertEqual(clean_text(text), "visit great day")

    def test_returns_empty_text_when_input_contains_only_removed_content(self) -> None:
        self.assertEqual(clean_text("https://example.com @User 123"), "")


if __name__ == "__main__":
    unittest.main()
