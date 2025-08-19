import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("<p>", "this is a value", ["test", 1, 1.2], {"key": "testme", "key2": "testmeagain"})
        self.assertEqual(node.tag, "<p>")
        self.assertEqual(node.value, "this is a value")
        self.assertEqual(node.children, ["test", 1, 1.2])
        self.assertEqual(node.props, {"key": "testme", "key2": "testmeagain"})

    def test_neq(self):
        tag = "<p>"
        value = "my value"
        children = ["TEST", "POK", "EMON"]
        props = {"key": "testme", "key2": "testmeagain"}
        node1 = HTMLNode(tag, value, children, props)
        node2 = HTMLNode(value=value, children=children, props=props)
        node3 = HTMLNode(tag=tag, props=props)
        self.assertNotEqual(node1.tag, node2.tag)
        self.assertNotEqual(node1.value, node3.value)
        self.assertNotEqual(node1.children, node3.children)

    def test_prop_to_html(self):
        node1 = HTMLNode(props={"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node1.props_to_html(), ' href="https://www.google.com" target="_blank"')
        node2 = HTMLNode()
        self.assertNotEqual(node1.props_to_html(), node2.props_to_html())
        self.assertEqual(node2.props_to_html(), '')

if __name__ == "__main__":
    unittest.main()