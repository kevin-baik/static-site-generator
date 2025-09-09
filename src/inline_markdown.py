from textnode import TextType, TextNode

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

