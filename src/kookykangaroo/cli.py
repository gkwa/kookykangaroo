"""Command line interface for KookyKangaroo."""

import sys

import dotenv
import typer

from kookykangaroo.credentials import get_neo4j_credentials
from kookykangaroo.logger import get_logger
from kookykangaroo.markdown_parser import MarkdownParser
from kookykangaroo.neo4j_graph import Neo4jGraph
from kookykangaroo.traversal import GraphTraversal

# Load environment variables from .env file
dotenv.load_dotenv()

app = typer.Typer(add_completion=False)
logger = get_logger()


def _setup_verbosity(verbose: int) -> None:
    """Set up verbosity level."""
    if verbose == 1:
        logger.set_level("INFO")
    elif verbose == 2:
        logger.set_level("DEBUG")
    elif verbose >= 3:
        logger.set_level("TRACE")


@app.callback()
def callback(
    verbose: int = typer.Option(
        0, "--verbose", "-v", count=True, help="Increase verbosity level."
    ),
) -> None:
    """Parse Markdown files into Neo4j graphs and traverse them."""
    _setup_verbosity(verbose)


@app.command()
def create_graph(
    file: str = typer.Option(..., "--file", "-f", help="Markdown file to parse."),
    uri: str = typer.Option(None, "--uri", "-u", help="Neo4j URI."),
    username: str = typer.Option(None, "--username", help="Neo4j username."),
    password: str = typer.Option(None, "--password", help="Neo4j password."),
) -> None:
    """Create a Neo4j graph from a markdown file."""
    try:
        # Get credentials from dedicated module
        uri, username, password = get_neo4j_credentials(uri, username, password)

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        parser = MarkdownParser()
        ast = parser.parse(content)

        graph = Neo4jGraph(uri, username, password)
        graph.connect()
        graph.create_graph(ast)
        graph.disconnect()

    except Exception as e:
        logger.error(f"Error creating graph: {e}")
        sys.exit(1)


@app.command()
def traverse_graph(
    uri: str = typer.Option(None, "--uri", "-u", help="Neo4j URI."),
    username: str = typer.Option(None, "--username", help="Neo4j username."),
    password: str = typer.Option(None, "--password", help="Neo4j password."),
) -> None:
    """Traverse a graph and print it as markdown."""
    try:
        # Get credentials from dedicated module
        uri, username, password = get_neo4j_credentials(uri, username, password)

        graph = Neo4jGraph(uri, username, password)
        graph.connect()

        traversal = GraphTraversal(graph)
        markdown = traversal.traverse_and_print()

        # Print to stdout for capture
        print(markdown)

        graph.disconnect()

    except Exception as e:
        logger.error(f"Error traversing graph: {e}")
        sys.exit(1)
