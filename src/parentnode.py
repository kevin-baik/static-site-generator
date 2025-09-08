from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        
        if not self.children:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            for child in self.children:
                return f"<{self.tag}{self.props_to_html()}>{child.to_html()}</{self.tag}>"

