import re
from textnode import TextType, TextNode

# input: text | <string>
# output: List<TextNode>
def text_to_textnodes(text):
    textnodes = [TextNode(text, TextType.TEXT)]
    textnodes = split_nodes_delimiter(textnodes, "**", TextType.BOLD)
    textnodes = split_nodes_delimiter(textnodes, "_", TextType.ITALIC)
    textnodes = split_nodes_delimiter(textnodes, "`", TextType.CODE)
    textnodes = split_nodes_image(textnodes)
    textnodes = split_nodes_link(textnodes)
    return textnodes

# input: List<TextNode>, <string>, <TextType>
# output: List<TextNode>
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise Exception(f"Syntax Error: missing '{delimiter}' closure")
            continue
        
        new_nodes.extend(text_delimiter(node.text, delimiter, text_type))
    return new_nodes

# input: <string>, <string>, <TextType>
# output: List<TextNode>
def text_delimiter(text, delimiter, text_type):
    new_nodes = []
    if text.count(delimiter) == 0:
        new_nodes.append(TextNode(text, TextType.TEXT))
        return new_nodes

    part_1, delim, part_2 = text.partition(delimiter)
    if delim:
        # delim is at front of text
        if not part_1:
            split = part_2.split(delimiter, 1)
            new_nodes.append(TextNode(split[0], text_type))
            if len(split) >= 1 and split[1] != "":
                new_nodes.extend(text_delimiter(split[1], delimiter, text_type))

        # delim is in the middle of text, part_1 is Text, part_2 contains delim word
        else:
            new_nodes.append(TextNode(part_1, TextType.TEXT))
            new_nodes.extend(text_delimiter(delim + part_2, delimiter, text_type))
    
    return new_nodes

# input: List<TextNode>
# output: List<TextNode>
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        image_list = extract_markdown_images(node.text)
        if not image_list:
            new_nodes.append(node)
            continue

        current_idx = 0
        for image in image_list:
            img_url = f"![{image[0]}]({image[1]})"
            start_idx = node.text.find(img_url)
            end_idx = start_idx + len(img_url)
            if start_idx > current_idx:
                new_nodes.append(TextNode(node.text[current_idx:start_idx], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            current_idx = end_idx

        if current_idx < len(node.text):
            new_nodes.append(TextNode(node.text[current_idx:], TextType.TEXT))
        
    return new_nodes

# input: List<TextNode>
# output: List<TextNode>
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        link_list = extract_markdown_links(node.text)
        if not link_list:
            new_nodes.append(node)
            continue

        current_idx = 0
        for link in link_list:
            link_url = f"[{link[0]}]({link[1]})"
            start_idx = node.text.find(link_url)
            end_idx = start_idx + len(link_url)
            if start_idx > current_idx:
                new_nodes.append(TextNode(node.text[current_idx:start_idx], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            current_idx = end_idx

        if current_idx < len(node.text):
            new_nodes.append(TextNode(node.text[current_idx:], TextType.TEXT))

    return new_nodes

# input: <string>
# output: List<string>
def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


# input: <string>
# output: List<string>
def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
