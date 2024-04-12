from typing import Any, Dict
import Sofa

from SofaRender.graph.graph_dict import GraphDict


class SofaGraph:

    def __init__(self, root_node: Sofa.Core.Node):
        self.graph = GraphDict()
        self.__explore_graph(root_node, 'root')
        self.root = root_node

    def __explore_graph(self, node: Sofa.Core.Node, parent: str):

        self.graph[parent] = {}

        if len(node.objects) > 0:
            components = {}
            for component in node.objects:
                name, class_name = component.getName(), component.getClassName()
                name = '...' if name == class_name else name
                components[f'{class_name}<{name}>'] = component
            self.graph[f'{parent}.@'] = components

        if len(node.children) > 0:
            for child in node.children:
                self.__explore_graph(child, child.name.value if parent is None else f'{parent}.{child.name.value}')

    def __repr__(self):
        desc = "SofaGraph(\n"
        indt = '  '

        def format_dict(res, graph: Dict[str, Any], indent: str):
            for key, value in graph.items():
                res += f"{indent}'{key}'"
                if isinstance(value, dict):
                    res += '\n'
                    res = format_dict(res, value, indent + '  ')
                else:
                    res += f':  {value}\n'
            return res

        desc = format_dict(desc, self.graph.store, indt)
        desc += ')'
        return desc
