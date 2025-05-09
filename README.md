# KookyKangaroo

A tool to parse Markdown files into Neo4j graphs and traverse them.

## Cheatsheet

```bash
# Create a Neo4j graph from a markdown file
kookykangaroo create-graph --file README.md --uri bolt://localhost:7687

# Traverse a graph and print it as markdown
kookykangaroo traverse-graph --uri bolt://localhost:7687

# You can also use environment variables or .env file
# NEO4J_URI=bolt://localhost:7687
# NEO4J_USERNAME=neo4j
# NEO4J_PASSWORD=your-password
```

## Installation

```bash
pip install kookykangaroo
```

## Quick Start

1. Start a Neo4j instance
2. Configure credentials in .env file or environment variables
3. Create a graph from your markdown file
4. Traverse the graph to see the original structure

## Environment Variables

You can set the following environment variables:

- `NEO4J_URI`: The Neo4j connection URI
- `NEO4J_USERNAME`: The Neo4j username
- `NEO4J_PASSWORD`: The Neo4j password
```

This markdown version contains the same content as the org-mode version but formatted according to Markdown syntax.
