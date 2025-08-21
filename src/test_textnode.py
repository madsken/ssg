import unittest

from textnode import TextNode, TextType, text_node_to_html_node

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

class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("A url", TextType.LINK, "url.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "A url")
        self.assertEqual(html_node.props["href"], "url.com")
    
    def test_img(self):
        node = TextNode("Alt text", TextType.IMAGE, "image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "image.png")
        self.assertEqual(html_node.props["alt"], "Alt text")

    def test_wrong_type(self):
        node = TextNode("Alt text", "Wrong text type")
        result = ""
        try:
            result = text_node_to_html_node(node)
        except Exception as e:
            result = str(e)
        self.assertEqual(result, "TextType did not match cases")

if __name__ == "__main__":
    unittest.main()