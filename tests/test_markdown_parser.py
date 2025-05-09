"""Test markdown parser module."""

import unittest

from kookykangaroo.markdown_parser import MarkdownParser


class TestMarkdownParser(unittest.TestCase):
    """Test MarkdownParser class."""

    def test_parse_simple_markdown(self) -> None:
        """Test parsing simple markdown."""
        markdown_content = """
# Header 1
Some paragraph

## Header 2
Another paragraph
"""
        parser = MarkdownParser()
        root = parser.parse(markdown_content)

        # Check root node
        self.assertEqual(root.node_type, "root")

        # Check children
        self.assertEqual(len(root.children), 1)
        self.assertEqual(root.children[0].node_type, "heading")
        self.assertEqual(root.children[0].content, "Header 1")
        self.assertEqual(root.children[0].level, 1)

        # Check grandchildren
        self.assertEqual(len(root.children[0].children), 2)
        self.assertEqual(root.children[0].children[0].node_type, "paragraph")
        self.assertEqual(root.children[0].children[0].content, "Some paragraph")

        self.assertEqual(root.children[0].children[1].node_type, "heading")
        self.assertEqual(root.children[0].children[1].content, "Header 2")
        self.assertEqual(root.children[0].children[1].level, 2)


if __name__ == "__main__":
    unittest.main()
