from typing import Any
from collections.abc import MutableMapping


class GraphDict(MutableMapping):

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
