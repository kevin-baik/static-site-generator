from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def __repr__(self):
        return(f"TextNode({self.text}, {self.text_type.value}, {self.url})")

# input: <TextNode>
# output: <LeafNode>
def text_node_to_html_node(text_node):
    tag = None
    value = None
    props = None
    
    match text_node.text_type:
        case TextType.TEXT:
            value = text_node.text
        case TextType.BOLD:
            tag = "b"
            value = text_node.text
        case TextType.ITALIC:
            tag = "i"
            value = text_node.text
        case TextType.CODE:
            tag = "code"
            value = text_node.text
        case TextType.LINK:
            tag = "a"
            value = text_node.text
            props = {"href": text_node.url}
        case TextType.IMAGE:
            tag = "img"
            value = ""
            props = {"alt": text_node.text, "src": text_node.url}
        case _:
            raise ValueError("Text type not recognized")
    
    return LeafNode(tag, value, props)


