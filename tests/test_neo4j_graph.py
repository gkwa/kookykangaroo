"""Test neo4j graph module."""

import unittest
import unittest.mock

from kookykangaroo.markdown_parser import MarkdownNode
from kookykangaroo.neo4j_graph import Neo4jGraph


class TestNeo4jGraph(unittest.TestCase):
    """Test Neo4jGraph class."""

    def setUp(self) -> None:
        """Set up test case."""
        self.graph = Neo4jGraph("bolt://localhost:7687", "neo4j", "neo4j")

        # Create a mock driver
        mock_driver = unittest.mock.MagicMock()
        mock_session = unittest.mock.MagicMock()
        mock_result = unittest.mock.MagicMock()

        mock_driver.session.return_value.__enter__.return_value = mock_session
        mock_session.run.return_value = mock_result

        self.graph.driver = mock_driver

    def test_generate_cypher_script(self) -> None:
        """Test generating Cypher script."""
        # Create a simple AST
        root = MarkdownNode("root")
        h1 = MarkdownNode("heading", "Header 1", 1)
        p1 = MarkdownNode("paragraph", "Paragraph 1")
        h2 = MarkdownNode("heading", "Header 2", 2)

        root.add_child(h1)
        h1.add_child(p1)
        h1.add_child(h2)

        # Generate script
        script = self.graph.get_cypher_script(root)

        # Check script contains expected parts
        self.assertIn("MATCH (n) DETACH DELETE n", script)
        self.assertIn("CREATE (node_0:Node", script)
        self.assertIn("CREATE (parent)-[:CONTAINS]->(child)", script)


if __name__ == "__main__":
    unittest.main()
