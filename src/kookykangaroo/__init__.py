"""KookyKangaroo - Parse Markdown files into Neo4j graphs and traverse them."""

try:
    from importlib.metadata import version as _version

    __version__ = _version("kookykangaroo")
except ImportError:
    # Fallback for older Python versions or when package is not installed
    __version__ = "unknown"

from kookykangaroo.cli import app

# Re-export app as main
main = app
