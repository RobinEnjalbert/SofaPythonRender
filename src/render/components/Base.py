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
        self.dirty_flags: Dict[str, bool] = {}
        self.vedo_object: Optional[Points] = None

    def create(self) -> None:
        raise NotImplementedError

    def update(self, idx: Optional[int]) -> None:
        raise NotImplementedError
