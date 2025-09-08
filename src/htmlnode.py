

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = []
        for key, value in self.props.items():
            props_html.append(f'{key}="{value}"')
        return " ".join(props_html)

    def __repr__(self):
        return (
            f"""
            ==HTML Node==
            tag: {self.tag}
            value: {self.value}
            children: {self.children}
            props: {self.props}
            """
        )
