from typing import Any, Dict
from collections.abc import MutableMapping
import Sofa


class CustomDict(MutableMapping):

    def __init__(self):
        self.__D = dict()

    @property
    def store(self):
        return self.__D.copy()

    def __getitem__(self, key: str):
        keys = key.split('.')
        _D = self.__D
        for k in keys[:-1]:
            _D = _D[k]
        return _D[keys[-1]]

    def __setitem__(self, key: str, value: Any):
        keys = key.split('.')
        _D = self.__D
        for k in keys[:-1]:
            _D = _D[k]
        _D[keys[-1]] = value

    def __delitem__(self, key: str):
        keys = key.split('.')
        _D = self.__D
        for k in keys[:-1]:
            _D = _D[k]
        del _D[keys[-1]]

    def __iter__(self):
        return iter(self.__flatten())

    def __len__(self):
        return len(self.__flatten())

    def items(self):
        return self.__flatten().items()

    def __flatten(self):

        def flat_dict(d, parent=None):
            res = {}
            for key, value in d.items():
                key = key if parent is None else f'{parent}.{key}'
                if isinstance(value, dict):
                    res = {**res, **flat_dict(value, key)}
                else:
                    res[key] = value
            return res

        return flat_dict(self.__D)


class SofaGraph:

    def __init__(self, root_node: Sofa.Core.Node):
        self.graph = CustomDict()
        self.__explore_graph(root_node, 'root')

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
