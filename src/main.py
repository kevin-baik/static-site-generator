from textnode import TextNode, TextType

def main():
    test_values = ("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    test_node = TextNode(*test_values)
    print(test_node)


if __name__ == "__main__":
    main()
