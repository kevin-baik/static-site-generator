from textnode import TextNode, TextType
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode


def main():
    test_values = ("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    test_node = TextNode(*test_values)
    print(test_node)


if __name__ == "__main__":
    main()
