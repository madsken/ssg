import unittest
from generate_html import extract_title
class TestExtractTitle(unittest.TestCase):
    def test_correct(self):
        markdown = "# A header"
        title = extract_title(markdown)
        self.assertEqual(title, "A header")

    def test_incorrect(self):
        markdown = "A header"
        with self.assertRaises(ValueError):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()