import unittest

from src.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            "a",
            "Google",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )
    def test_props_to_html_empty_dict(self):
        node = HTMLNode("p", "hello", None, {})
        self.assertEqual(node.props_to_html(), "")
    def test_props_to_html_none(self):
        node = HTMLNode("p", "hello")
        self.assertEqual(node.props_to_html(), "")
    def test_props_to_html_single_prop(self):
        node = HTMLNode("img", None, None, {"src": "logo.png"})
        self.assertEqual(node.props_to_html(), ' src="logo.png"')

if __name__ == "__main__":
    unittest.main()