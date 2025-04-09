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
    result = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
            
        current_text = old_node.text
        matches = extract_markdown_images(current_text)
        
        if not matches:
            result.append(old_node)
            continue
            
        for alt_text, url in matches:
            parts = current_text.split(f"![{alt_text}]({url})", 1)
            
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
                
            result.append(TextNode(alt_text, TextType.IMAGE, url))
            
            current_text = parts[1] if len(parts) > 1 else ""
       
        if current_text:
            result.append(TextNode(current_text, TextType.TEXT))
            
    return result

def split_nodes_link(old_nodes):
    result = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
            
        current_text = old_node.text
        matches = extract_markdown_links(current_text)
        
        if not matches:
            result.append(old_node)
            continue
            
        for text, url in matches:
            parts = current_text.split(f"[{text}]({url})", 1)
            
            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
                
            result.append(TextNode(text, TextType.LINK, url))
            
            current_text = parts[1] if len(parts) > 1 else ""
       
        if current_text:
            result.append(TextNode(current_text, TextType.TEXT))
            
    return result

def extract_markdown_images(text):
    image_re = re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")
    return re.findall(image_re, text)

def extract_markdown_links(text):
    link_re = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)")
    return re.findall(link_re, text)

def text_to_textnodes(text):
    og_textnode = TextNode(text, TextType.TEXT)
    nodes = split_nodes_image([og_textnode])
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    return nodes
