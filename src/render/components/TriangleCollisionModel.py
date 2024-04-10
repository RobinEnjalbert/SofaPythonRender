from typing import Optional
from vedo import Mesh

from SofaRender.render.components.Base import BaseConfig, BaseComponent
from SofaRender.render.remote.vedo_memory import VedoMemory
from SofaRender.render.settings import STYLES


class Config(BaseConfig):

    def __init__(self):
        super().__init__()
        self.add_linked_fields(link_name='state', field_names=['position'])
        self.add_linked_fields(link_name='topology', field_names=['triangles'])


class Component(BaseComponent):
    category: str = 'collision_models'

    def __init__(self, data: VedoMemory):
        BaseComponent.__init__(self, data=data)

    def create(self) -> None:

        # Access Data fields
        positions = self.data.get_data(link_name='state', field_name='position')[0]
        triangles = self.data.get_data(link_name='topology', field_name='triangles')[0]

        # Create the Vedo Actor
        self.vedo_object = Mesh(inputobj=[positions, triangles],
                                c=STYLES[self.category]['color']
                                , alpha=STYLES[self.category]['alpha']).wireframe(True).lw(2)

    def update(self, idx: Optional[int] = None) -> None:

        position, dirty = self.data.get_data(link_name='state', field_name='position')
        if dirty:
            self.vedo_object.vertices = position
