from typing import Optional, Dict, List
from vedo import Plotter, Points
from numpy import ndarray

from SofaRender.render.remote.vedo_memory import VedoMemory


class BaseConfig:

    def __init__(self):
        self.object_fields: List[str] = []
        self.linked_fields: Dict[str, List[str]] = {}

    def add_object_fields(self, field_names: List[str]):

        self.object_fields += field_names

    def add_linked_fields(self, link_name: str, field_names: List[str]):

        self.linked_fields[link_name] = field_names


class BaseComponent:
    category: str = ''

    def __init__(self, data: VedoMemory):

        self.data = data
        self.memory: Dict[str, ndarray] = {}
        self.dirty_flags: Dict[str, bool] = {}
        self.vedo_object: Optional[Points] = None

    def create(self) -> None:
        raise NotImplementedError

    def update(self, idx: Optional[int]) -> None:
        raise NotImplementedError

    def read_memory(self) -> None:
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
