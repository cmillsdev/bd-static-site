class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        prop_string = ""
        if self.props:
            for key, value in self.props.items():
                prop_string += f' {key}="{value}" '
        return prop_string

    def __repr__(self):
        return f"HTMLNode(tags={self.tag} value={self.value} children={self.children} props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value=value, children=None, props=props)

    def to_html(self):
        # print(f"Rendering HtmlNode: {self.tag}, children: {len(self.children)}")
        if not self.value:
            print(self)
            raise ValueError
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        # print(f"Rendering HtmlNode: {self.tag}, children: {len(self.children)}")
        if not self.tag:
            raise ValueError("missing tag")
        if not self.children:
            raise ValueError("missing children")
        return f"<{self.tag}{self.props_to_html()}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"
