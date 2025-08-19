import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_with_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "url.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "url.com")
        self.assertEqual(node, node2)

    def test_text_neq(self):
        node = TextNode("Text 1", TextType.CODE)
        node2 = TextNode("Text 2", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_type_neq(self):
        node = TextNode("Text 1", TextType.CODE)
        node2 = TextNode("Text 1", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_url_neq(self):
        node = TextNode("This is a text node", TextType.BOLD, "url1.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "url2.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()