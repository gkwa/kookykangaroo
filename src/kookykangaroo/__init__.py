"""KookyKangaroo - Parse Markdown files into Neo4j graphs and traverse them."""

__version__ = "0.1.0"

from kookykangaroo.cli import app

# Re-export app as main
main = app
