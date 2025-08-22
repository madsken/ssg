from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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
    
def markdown_to_blocks(md_doc):
    split_doc = md_doc.split("\n\n")
    stripped_doc = []
    for doc in split_doc:
        if len(doc) != 0:
            stripped_doc.append(doc.strip())
    return stripped_doc

##Note. Could have been a simpler solution using .startswith()
def block_to_blocktype(block):
    #Match headers
    match = re.fullmatch(r"^(#{1,6})\s+(.*)", block)
    if match is not None:
        if block == match.string:
            return BlockType.HEADING
    #Match code blocks
    match = re.fullmatch(r"```[\s\S]*?```", block)
    if match is not None:
        if block == match.string:
            return BlockType.CODE

    #Check if quote block
    if block[0] == ">":
        lines = block.split("\n")
        for line in lines:
            if line[0] != ">":
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    #Check if unordered list block
    if block[:2] == "- ":
        lines = block.split("\n")
        for line in lines:
            if line[:2] != "- ":
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    #check for ordered list block
    for line in block.split("\n"):
        match = re.findall(r"^\d+\.\s+.+$", line)
        if len(match) == 0:
            return BlockType.PARAGRAPH
    return BlockType.ORDERED_LIST


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    root_children = []
    for block in blocks:
        html_node = block_to_htmlnode(block)
        root_children.append(html_node)
    return ParentNode("div", root_children)

def block_to_htmlnode(block):
    blocktype = block_to_blocktype(block)
    if blocktype ==  BlockType.PARAGRAPH:
        return paragraph_to_htmlnode(block)
    if blocktype ==  BlockType.HEADING:
        return heading_to_htmlnode(block)
    if blocktype ==  BlockType.CODE:
        return code_to_htmlnode(block)
    if blocktype ==  BlockType.QUOTE:
        return quote_to_htmlnode(block)
    if blocktype ==  BlockType.UNORDERED_LIST:
        return ul_to_htmlnode(block)
    if blocktype ==  BlockType.ORDERED_LIST:
        return ol_to_htmlnode(block)
    raise ValueError(f"invalid blocktype passed: {blocktype}")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children

def paragraph_to_htmlnode(block):
    text = " ".join(block.split("\n"))
    children = text_to_children(text)
    return ParentNode("p", children)

def heading_to_htmlnode(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1: ]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_htmlnode(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block, does not start or end with ```")
    text = block[4:-3]
    child = [text_node_to_html_node(TextNode(text, TextType.TEXT))] #Important: Has to be added to a list (hence the [])
    code_node = [ParentNode("code", child)] #Important: Has to be added to a list (hence the [])
    return ParentNode("pre", code_node) #<pre> tag is for formatting so the text has the same size i think???

def quote_to_htmlnode(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Wrong quotation formatting")
        new_lines.append(line.lstrip(">").strip())
    text = " ".join(new_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)
     
def ul_to_htmlnode(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ul", list_items)

def ol_to_htmlnode(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        text = line[3:]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ol", list_items)


if __name__ == "__main__":
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
    markdown_to_html_node(md)