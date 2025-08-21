from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    split_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            split_nodes.append(old_node)
            continue

        split_node = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid text, contains non enclosed section")

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_node.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_node.append(TextNode(sections[i], text_type))
        split_nodes.extend(split_node)
    return split_nodes

def split_nodes_image(old_nodes):
    split_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            split_nodes.append(old_node)
            continue
        original_text = old_node.text
        image_sections = extract_markdown_images(old_node.text)
        if image_sections is None:
            split_nodes.append(old_node)
            continue
        for image in image_sections:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]
        if original_text != "":
            split_nodes.append(TextNode(original_text, TextType.TEXT))
    return split_nodes

def split_nodes_link(old_nodes):
    split_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            split_nodes.append(old_node)
            continue
        original_text = old_node.text
        link_sections = extract_markdown_links(old_node.text)
        if link_sections is None:
            split_nodes.append(old_node)
            continue
        for link in link_sections:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            split_nodes.append(TextNode(original_text, TextType.TEXT))
    return split_nodes

def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    nodes = [text_node]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
    


if __name__ == "__main__":
    nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
    for node in nodes:
        print(node)