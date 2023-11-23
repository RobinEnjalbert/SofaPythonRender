from typing import Optional, Dict
import Sofa
from vedo import Points, Plotter
from numpy import ndarray


class BaseComponent:
    category: str = ''

    def __init__(self, sofa_object: Sofa.Core.Object, context: Dict[str, Sofa.Core.Object]):

        self.sofa_object: Sofa.Core.Object = sofa_object
        self.vedo_object: Optional[Points] = None

        self.memory: Dict[str, ndarray] = {}

    def update(self, plt: Plotter, idx: Optional[int] = None) -> None:
        raise NotImplementedError

    def store(self, **kwargs) -> None:
        if len(self.memory) == 0:
            self.memory = {key: [value] for key, value in kwargs.items()}
        else:
            for key, value in kwargs.items():
                self.memory[key].append(value)

    def reset_memory(self) -> None:
        self.memory = {key: [value[0]] for key, value in self.memory.items()}

    def get_item(self, idx: int) -> Dict[str, ndarray]:
        return {key: value[idx] for key, value in self.memory.items()}
