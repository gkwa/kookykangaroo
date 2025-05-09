"""Markdown parser module."""

import typing

import markdown
import markdown.treeprocessors
import xml.etree.ElementTree as ET


class MarkdownNode:
    """Represents a node in the markdown AST."""

    def __init__(
        self,
        node_type: str,
        content: str = "",
        level: int = 0,
        parent: typing.Optional["MarkdownNode"] = None,
    ) -> None:
        """Initialize a markdown node."""
        self.node_type = node_type
        self.content = content
        self.level = level
        self.parent = parent
        self.children = []
        self.id = None  # Will be set when creating Neo4j nodes

    def add_child(self, child: "MarkdownNode") -> None:
        """Add a child node."""
        child.parent = self
        self.children.append(child)


class MarkdownTreeProcessor(markdown.treeprocessors.Treeprocessor):
    """Tree processor for extracting markdown structure."""

    def __init__(self, md: markdown.Markdown) -> None:
        """Initialize the tree processor."""
        super().__init__(md)
        self.root = MarkdownNode("root")
        self.current_node = self.root
        self.heading_stack = [self.root]

    def run(self, root: ET.Element) -> ET.Element:
        """Process the element tree."""
        self._process_element(root)
        return root

    def _process_element(self, element: ET.Element) -> None:
        """Process an element and its children."""
        if element.tag.startswith("h") and len(element.tag) == 2:
            # Handle heading
            level = int(element.tag[1])
            content = "".join(element.itertext()).strip()

            # Pop stack until we find a heading of lower level
            while len(self.heading_stack) > 1 and self.heading_stack[-1].level >= level:
                self.heading_stack.pop()

            # Create new heading node
            node = MarkdownNode("heading", content, level)
            self.heading_stack[-1].add_child(node)
            self.heading_stack.append(node)
            self.current_node = node
        elif element.tag == "p":
            # Handle paragraph
            content = "".join(element.itertext()).strip()
            if content:
                node = MarkdownNode("paragraph", content)
                self.current_node.add_child(node)

        # Process child elements
        for child in element:
            self._process_element(child)


class MarkdownParser:
    """Parse markdown into a tree structure."""

    def __init__(self) -> None:
        """Initialize the markdown parser."""
        self.md = markdown.Markdown(extensions=["extra"])

    def parse(self, content: str) -> MarkdownNode:
        """Parse markdown content into a tree structure."""
        processor = MarkdownTreeProcessor(self.md)
        self.md.treeprocessors.register(processor, "ast_extractor", 175)

        # Parse the markdown to trigger the processor
        self.md.convert(content)

        return processor.root
