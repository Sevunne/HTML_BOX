from bs4 import BeautifulSoup, NavigableString, Tag

# ---------------------------
# 【上线前修改】替换为你真实节点类导入
# from block_nodes import BaseDomNode, HtmlNode, HeadNode, BodyNode, PNode
# ---------------------------
class BaseDomNode:
    def __init__(self, tag_name: str):
        self.tag_name = tag_name
        self.attrs: dict[str, str] = {}
        self.children: list = []
        self.inner_text: str = ""

    def add_child(self, child):
        self.children.append(child)


def html_to_node_tree(html_source: str) -> BaseDomNode | None:
    """
    HTML字符串 → 积木节点树
    使用场景：代码编辑器 → 切换积木模式
    """
    soup = BeautifulSoup(html_source, "html.parser")
    html_tag = soup.find("html")
    if not html_tag:
        return None

    def tag_to_node(bs_tag: Tag) -> BaseDomNode:
        tag_name = bs_tag.name
        # =========标签映射区域=========
        if tag_name == "html":
            node = BaseDomNode("html")
        elif tag_name == "head":
            node = BaseDomNode("head")
        elif tag_name == "body":
            node = BaseDomNode("body")
        elif tag_name == "p":
            node = BaseDomNode("p")
        else:
            node = BaseDomNode(tag_name)
        # =============================
        node.attrs = dict(bs_tag.attrs)

        text_buf = []
        for item in bs_tag.contents:
            if isinstance(item, NavigableString):
                text_buf.append(str(item))
            elif isinstance(item, Tag):
                child_node = tag_to_node(item)
                node.add_child(child_node)
        node.inner_text = "".join(text_buf)
        return node

    root_node = tag_to_node(html_tag)
    return root_node


def node_tree_to_html(root_node: BaseDomNode) -> str:
    """
    积木节点树 → HTML源码字符串
    使用场景：积木模式 → 切回代码编辑器
    """
    if not root_node:
        return "<html><head></head><body></body></html>"

    def render(node: BaseDomNode) -> str:
        attr_text = ""
        if node.attrs:
            attr_list = [f'{k}="{v}"' for k, v in node.attrs.items()]
            attr_text = " " + " ".join(attr_list)
        inner_content = node.inner_text
        for child in node.children:
            inner_content += render(child)
        return f"<{node.tag_name}{attr_text}>{inner_content}</{node.tag_name}>"

    return render(root_node)


# 本地自测入口
if __name__ == "__main__":
    test_code = """
<html>
<head></head>
<body>
    <p>我是布丁</p>
</body>
</html>
    """
    tree = html_to_node_tree(test_code)
    output_html = node_tree_to_html(tree)
    print(output_html)
