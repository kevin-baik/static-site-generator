from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        
        html_output = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html_output

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

