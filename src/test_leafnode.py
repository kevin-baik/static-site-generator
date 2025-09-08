import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node2 = LeafNode("a", "Google it!", {"href": "https://www.google.com"})
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Google it!</a>')
    
    def test_leaf_value_error(self):
        node = LeafNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_only_value(self):
        node = LeafNode(None, "Node with only value")
        self.assertEqual(node.to_html(), "Node with only value")


if __name__ == "__main__":
    unittest.main()
