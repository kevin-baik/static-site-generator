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
    CODE = "code", "code", {"pre": True}
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
        (BlockType.HEADING, r"(?P<number>^#{1,6}) (?P<heading>.*)"),
        (BlockType.CODE, r"^`{3}(?P<code>[\s\S]*)`{3}$"),
        (BlockType.QUOTE, r"(?P<quote>^>.*)"),
        (BlockType.UNORDERED_LIST, r"(?<=^- )(?: *)(?P<ul_item>.*)"),
        (BlockType.ORDERED_LIST, r"(?P<rank>^\d)(?:\. *)(?P<ol_item>.*)"),
    ]
    match_type = BlockType.PARAGRAPH
    for regex in block_regex:
        match = re.search(regex[1], block)
        if match:
            if regex[0] is BlockType.ORDERED_LIST:
                print("\tordered_list_rank: ", match['rank'])
                if match['rank'] != "1":
                    raise IndexError("List Index Error: Ordered list must start with 1.")
            match_type = regex[0]
            break
    print(f"MATCHED :: {match_type} : {match}")
    return match_type

# input: markdown | <string>
# output: parent HTMLNode with nested child HTMLNodes | <string>
def markdown_to_html_node(markdown):
    children_nodes = []
    blocks = markdown_to_blocks(markdown)
    print("================================================================")
    print(markdown)
    print(f"Blocks: {blocks}")
    for block in blocks:
        block_type = block_to_block_type(block)
        print(f"\tCURRENT_BLOCK:\n{block}")
        html_nodes = []
        if block_type is BlockType.CODE:
            html_nodes = split_nodes_delimiter([TextNode(block, TextType.TEXT)], "`", TextType.CODE)
        else:
            html_nodes = text_to_children(block)
        print()
        print(html_nodes)
        html_text = "".join(map(lambda node: node.to_html(), html_nodes))
        print(f"HTML_TEXT: {html_text}")
        children_nodes.append(ParentNode(block_type.tag, html_nodes))

    
    print(f"****** CHILDREN ******")
    print(children_nodes)
    result = ParentNode("div", children_nodes)
    print()
    print(f"$$$$$$$ RESULT $$$$$$$")
    print(result)
    print(result.to_html())
    return result

# input: markdown text | <string>
# output: [LeafNode] | List<LeafNode>
def text_to_children(text):
    print(f"!---!---FUNCTION: text_to_children({text.replace('\n', ' ')})")
    html_nodes = []
    text_nodes = text_to_textnodes(text.replace('\n', ' '))
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

