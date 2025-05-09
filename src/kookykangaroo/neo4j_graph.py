"""Neo4j graph module."""

import typing

import neo4j.graph

from kookykangaroo.logger import get_logger
from kookykangaroo.markdown_parser import MarkdownNode

logger = get_logger()


class Neo4jGraph:
    """Interface to Neo4j graph database."""

    def __init__(self, uri: str, username: str, password: str) -> None:
        """Initialize Neo4j connection."""
        self.uri = uri
        self.username = username
        self.password = password
        self.driver = None

    def connect(self) -> None:
        """Connect to Neo4j database."""
        try:
            self.driver = neo4j.GraphDatabase.driver(
                self.uri, auth=(self.username, self.password)
            )
            logger.info(f"Connected to Neo4j at {self.uri}")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise

    def disconnect(self) -> None:
        """Disconnect from Neo4j database."""
        if self.driver:
            self.driver.close()
            logger.info("Disconnected from Neo4j")

    def create_graph(self, root_node: MarkdownNode) -> None:
        """Create a graph from a markdown AST."""
        logger.info("Creating graph from markdown AST")

        # Clear existing graph
        self._execute_query("MATCH (n) DETACH DELETE n")

        # Create nodes
        self._create_nodes(root_node)

        # Create relationships
        self._create_relationships(root_node)

        logger.info("Graph creation completed")

    def _create_nodes(self, root_node: MarkdownNode) -> None:
        """Create nodes in Neo4j from markdown nodes."""
        # Create root node
        query = """
        CREATE (n:Node {id: $id, type: $type, content: $content})
        RETURN n
        """
        root_node.id = "node_0"
        self._execute_query(
            query,
            {
                "id": root_node.id,
                "type": root_node.node_type,
                "content": root_node.content,
            },
        )

        # Create other nodes with a stack-based approach
        stack = [(root_node, 0)]
        node_count = 1

        while stack:
            parent, child_index = stack.pop()

            if child_index < len(parent.children):
                # Process next child
                child = parent.children[child_index]
                stack.append((parent, child_index + 1))

                # Create node for child
                child.id = f"node_{node_count}"
                node_count += 1

                query = """
                CREATE (n:Node {id: $id, type: $type, content: $content, level: $level})
                RETURN n
                """
                self._execute_query(
                    query,
                    {
                        "id": child.id,
                        "type": child.node_type,
                        "content": child.content,
                        "level": child.level,
                    },
                )

                # Add this child's children to stack
                if child.children:
                    stack.append((child, 0))

    def _create_relationships(self, root_node: MarkdownNode) -> None:
        """Create relationships between nodes."""
        # Use a stack-based approach
        stack = [(root_node, 0)]

        while stack:
            parent, child_index = stack.pop()

            if child_index < len(parent.children):
                # Process next child
                child = parent.children[child_index]
                stack.append((parent, child_index + 1))

                # Create relationship
                query = """
                MATCH (parent:Node {id: $parent_id})
                MATCH (child:Node {id: $child_id})
                CREATE (parent)-[:CONTAINS]->(child)
                """
                self._execute_query(
                    query, {"parent_id": parent.id, "child_id": child.id}
                )

                # Add this child's children to stack
                if child.children:
                    stack.append((child, 0))

    def _execute_query(
        self, query: str, parameters: typing.Optional[dict] = None
    ) -> typing.List[typing.Dict]:
        """Execute a Cypher query."""
        if parameters is None:
            parameters = {}

        logger.debug(f"Executing query: {query}")

        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]

    def get_cypher_script(self, root_node: MarkdownNode) -> str:
        """Generate a Cypher script for creating the graph."""
        lines = []

        # Clear existing graph
        lines.append("// Clear existing graph")
        lines.append("MATCH (n) DETACH DELETE n;")
        lines.append("")

        # Create nodes
        lines.append("// Create nodes")
        node_queries = self._generate_node_queries(root_node)
        lines.extend(node_queries)
        lines.append("")

        # Create relationships
        lines.append("// Create relationships")
        rel_queries = self._generate_relationship_queries(root_node)
        lines.extend(rel_queries)

        return "\n".join(lines)

    def _generate_node_queries(self, root_node: MarkdownNode) -> typing.List[str]:
        """Generate Cypher queries for creating nodes."""
        queries = []

        # Assign IDs to nodes
        self._assign_node_ids(root_node)

        # Root node
        queries.append(
            "CREATE (node_0:Node {id: 'node_0', type: 'root', content: ''});"
        )

        # Generate queries for all nodes using a stack
        stack = [(root_node, 0)]
        node_count = 1

        while stack:
            parent, child_index = stack.pop()

            if child_index < len(parent.children):
                # Process next child
                child = parent.children[child_index]
                stack.append((parent, child_index + 1))

                # Create node for child
                child.id = f"node_{node_count}"
                node_count += 1

                query = (
                    f"CREATE (node_{node_count - 1}:Node {{id: 'node_{node_count - 1}', "
                    f"type: '{child.node_type}', content: '{self._escape_string(child.content)}'"
                )

                if child.level > 0:
                    query += f", level: {child.level}"

                query += "});"
                queries.append(query)

                # Add this child's children to stack
                if child.children:
                    stack.append((child, 0))

        return queries

    def _generate_relationship_queries(
        self, root_node: MarkdownNode
    ) -> typing.List[str]:
        """Generate Cypher queries for creating relationships."""
        queries = []

        # Use a stack-based approach
        stack = [(root_node, 0)]

        while stack:
            parent, child_index = stack.pop()

            if child_index < len(parent.children):
                # Process next child
                child = parent.children[child_index]
                stack.append((parent, child_index + 1))

                # Create relationship
                queries.append(
                    f"MATCH (parent:Node {{id: '{parent.id}'}})\n"
                    f"MATCH (child:Node {{id: '{child.id}'}})\n"
                    f"CREATE (parent)-[:CONTAINS]->(child);"
                )

                # Add this child's children to stack
                if child.children:
                    stack.append((child, 0))

        return queries

    def _assign_node_ids(self, root_node: MarkdownNode) -> None:
        """Assign IDs to nodes."""
        root_node.id = "node_0"
        node_count = 1

        # Use a stack-based approach
        stack = [(root_node, 0)]

        while stack:
            parent, child_index = stack.pop()

            if child_index < len(parent.children):
                # Process next child
                child = parent.children[child_index]
                stack.append((parent, child_index + 1))

                # Assign ID
                child.id = f"node_{node_count}"
                node_count += 1

                # Add this child's children to stack
                if child.children:
                    stack.append((child, 0))

    def _escape_string(self, s: str) -> str:
        """Escape a string for Cypher query."""
        return s.replace("'", "\\'")

    def get_root_node(self) -> typing.Dict:
        """Get the root node from the graph."""
        query = """
        MATCH (n:Node {type: 'root'})
        RETURN n
        """
        result = self._execute_query(query)
        if result:
            return result[0]["n"]
        return None

    def get_children(self, node_id: str) -> typing.List[typing.Dict]:
        """Get children of a node."""
        query = """
        MATCH (parent:Node {id: $node_id})-[:CONTAINS]->(child:Node)
        RETURN child
        ORDER BY child.level, child.id
        """
        result = self._execute_query(query, {"node_id": node_id})
        return [record["child"] for record in result]
