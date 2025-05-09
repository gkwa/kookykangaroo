"""Test graph traversal module."""

import unittest
import unittest.mock

from kookykangaroo.neo4j_graph import Neo4jGraph
from kookykangaroo.traversal import GraphTraversal


class TestGraphTraversal(unittest.TestCase):
    """Test GraphTraversal class."""

    def setUp(self) -> None:
        """Set up test case."""
        self.mock_graph = unittest.mock.MagicMock(spec=Neo4jGraph)
        self.traversal = GraphTraversal(self.mock_graph)

    def test_traverse_and_print(self) -> None:
        """Test traversing and printing graph."""
        # Set up mock return values
        self.mock_graph.get_root_node.return_value = {"id": "node_0", "type": "root"}
        self.mock_graph.get_children.side_effect = [
            # First call for root node
            [{"id": "node_1", "type": "heading", "content": "Header 1", "level": 1}],
            # Second call for node_1
            [
                {"id": "node_2", "type": "paragraph", "content": "Paragraph 1"},
                {"id": "node_3", "type": "heading", "content": "Header 2", "level": 2},
            ],
            # Third call for node_2
            [],
            # Fourth call for node_3
            [],
        ]

        # Call the method
        result = self.traversal.traverse_and_print()

        # Check result
        expected = "# Header 1\n\nParagraph 1\n\n## Header 2\n\n"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
