"""Graph traversal module."""

import typing

from kookykangaroo.logger import get_logger
from kookykangaroo.neo4j_graph import Neo4jGraph

logger = get_logger()


class GraphTraversal:
    """Traverse Neo4j graph and convert back to markdown."""

    def __init__(self, graph: Neo4jGraph) -> None:
        """Initialize the graph traversal."""
        self.graph = graph

    def traverse_and_print(self) -> str:
        """Traverse the graph and print as markdown."""
        logger.info("Traversing graph")

        # Get root node
        root_node = self.graph.get_root_node()
        if not root_node:
            logger.error("Root node not found in graph")
            return ""

        # Build markdown
        markdown_lines = []
        self._traverse_node(root_node["id"], markdown_lines)

        return "\n".join(markdown_lines)

    def _traverse_node(self, node_id: str, lines: typing.List[str]) -> None:
        """Recursively traverse nodes and build markdown."""
        # Get children of current node
        children = self.graph.get_children(node_id)

        for child in children:
            if child["type"] == "heading":
                level = child.get("level", 1)
                heading_prefix = "#" * level
                lines.append(f"{heading_prefix} {child['content']}")
                lines.append("")  # Empty line after heading
            elif child["type"] == "paragraph":
                lines.append(child["content"])
                lines.append("")  # Empty line after paragraph

            # Recursively process children
            self._traverse_node(child["id"], lines)
