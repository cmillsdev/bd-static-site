import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_htmlnode(self):
        node1 = HTMLNode(props={"href": "google.com", "target": "googs"})
        node2 = HTMLNode()
        print(node1)
        print(node1.props_to_html())
        print(node2)
    
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


if __name__ == "__main__":
    unittest.main()
