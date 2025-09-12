import re
from enum import Enum
from inline_markdown import text_to_textnodes, split_nodes_delimiter
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode
from parentnode import ParentNode

class HTMLEnum(Enum):
    def __new__(cls, type, tag, *args):
        obj = object.__new__(cls)
        obj._value_ = type
        obj.tag = tag
        obj.format = {}
        return obj

    def __init__(self, type, tag, *formats):
        if formats:
            self.format = formats[0]

class BlockType(HTMLEnum):
    PARAGRAPH = "paragraph", "p"
    HEADING = "heading", "h"
    CODE = "code", "pre", {"pre": True}
    QUOTE = "quote", "blockquote"
    UNORDERED_LIST = "unordered list", "ul", {"list": "li"}
    ORDERED_LIST = "ordered list", "ol", {"list": "li"}

           

# input: markdown | <string>
# output: [markdown block] | List<string>
def markdown_to_blocks(markdown):
    if not markdown:
        raise ValueError("markdown is empty")

    blocks = markdown.split("\n\n")
    if blocks[-1] == "":
        del blocks[-1]
    blocks = list(map(lambda block: block.strip(), blocks))
    return blocks

# input: markdown block | <string>
# output: BlockType of input block | <BlockType>
def block_to_block_type(block):
    block_regex = [
        (BlockType.HEADING, r"(?P<number>^#{1,6})(?P<heading>.*)"),
        (BlockType.CODE, r"^`{3}(?P<code>[\s\S]*)`{3}$"),
        (BlockType.QUOTE, r"(?P<quote>^>.*)"),
        (BlockType.UNORDERED_LIST, r"(?P<number>^- )(?: *)(?P<ul_item>.*)"),
        (BlockType.ORDERED_LIST, r"(?P<rank>^\d)(?:\. *)(?P<ol_item>.*)"),
    ]
    match_type = BlockType.PARAGRAPH
    for regex in block_regex:
        matches = re.findall(regex[1], block)
        print(f"REGEX_MATCHES: {matches}")
        if matches:
            if regex[0] is BlockType.UNORDERED_LIST:
                for match in matches:
                    if match[0] is None:
                        break
            if regex[0] is BlockType.ORDERED_LIST:
                current_rank = 0
                for match in matches:
                    current_rank += 1
                    if match[0] != current_rank:
                        break
                if matches[-1][0] == current_rank:
                    match_type = regex[0]
                    break 
            match_type = regex[0]
            break
    print(f"MATCHED :: {match_type}")
    return match_type

# input: markdown | <string>
# output: parent HTMLNode with nested child HTMLNodes | <string>
def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    print("================================================================")
    print(markdown)
    print(f"Blocks: {blocks}")
    for block in blocks:
        print(f"\tCURRENT_BLOCK:\n{block}")
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


# input: <string>
# output: <HTMLNode>
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

# input: markdown text | <string>
# output: [LeafNode] | List<LeafNode>
def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
