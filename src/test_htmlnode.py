import unittest

from htmlnode import LeafNode, ParentNode, HTMLNode


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

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")    
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")    
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")
    
    def test_leaf_to_html_i(self):
        node = LeafNode("i", "Hello, world!")    
        self.assertEqual(node.to_html(), "<i>Hello, world!</i>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_false(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertNotEqual(node.to_html(), '<a>Click me!</a>')
        node = LeafNode("a", "Click me!")
        self.assertNotEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_multiple_children_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        node = ParentNode(
            "p",
            [
                parent_node,
                parent_node,
                child_node,
                grandchild_node,
            ],
        )
        self.assertEqual(node.to_html(), "<p><div><span><b>grandchild</b></span></div><div><span><b>grandchild</b></span></div><span><b>grandchild</b></span><b>grandchild</b></p>")


if __name__ == "__main__":
    unittest.main()