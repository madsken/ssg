

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("Method not implemented")
    
    def props_to_html(self):
        res = ""
        if self.props is None:
            return res
        for prop in self.props:
            res += f' {prop}="{self.props[prop]}"'

        return res
    
    def __repr__(self):
        return f"HTMLNode(\ntag={self.tag}, \nvalue={self.value}, \nchildren={self.children}, \nprops={self.props})"