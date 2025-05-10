"""Credentials module for KookyKangaroo."""

import os


def get_neo4j_credentials(uri=None, username=None, password=None):
    """
    Get Neo4j credentials from parameters or environment variables.

    Args:
        uri: Neo4j URI, or None to use environment variable
        username: Neo4j username, or None to use environment variable
        password: Neo4j password, or None to use environment variable

    Returns:
        tuple: (uri, username, password)
    """
    uri = uri or os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    username = username or os.environ.get("NEO4J_USERNAME", "neo4j")
    password = password or os.environ.get("NEO4J_PASSWORD", "neo4j")

    return uri, username, password
