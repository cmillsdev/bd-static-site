import re
from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise ValueError("no matching text type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            node_text = node.text.split(delimiter)
            if len(node_text) % 2 == 0:
                raise ValueError("invalid markdown syntax")
            for i in range(len(node_text)):
                if node_text[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(node_text[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(node_text[i], text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    pass

def split_nodes_link(old_nodes):
    pass

def extract_markdown_images(text):
    image_re = re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")
    return re.findall(image_re, text)

def extract_markdown_links(text):
    link_re = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)")
    return re.findall(link_re, text)