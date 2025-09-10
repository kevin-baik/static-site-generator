import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

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
        (BlockType.HEADING, r"^#{1,6} (?P<heading>.*)"),
        (BlockType.CODE, r"^`{3}(?P<code>[\s\S]*)`{3}$"),
        (BlockType.QUOTE, r"(?P<quote>^>.*)"),
        (BlockType.UNORDERED_LIST, r"(?<=^- )(?: *)(?P<ul_item>.*)"),
        (BlockType.ORDERED_LIST, r"(?P<rank>^\d)(?:\. *)(?P<ol_item>.*)"),
    ]
    print("================================")
    match_type = BlockType.PARAGRAPH
    for regex in block_regex:
        print("matching... ", regex[0])
        match = re.search(regex[1], block)
        print("match complete... ", match) 
        if match:
            if regex[0] is BlockType.ORDERED_LIST:
                print("ordered_list_rank: ", match['rank'])
                if match['rank'] != "1":
                    raise IndexError("List Index Error: Ordered list must start with 1.")
            match_type = regex[0]
            break
    print("MATCHED: ", match_type)
    return match_type

