from typing import Optional
from vedo import Glyph, Box

from SofaRender.render.components.Base import BaseConfig, BaseComponent
from SofaRender.render.remote.vedo_memory import VedoMemory
from SofaRender.render.settings import STYLES


class Config(BaseConfig):

    def __init__(self):
        super().__init__()
        self.add_object_fields(field_names=['indices'])
        self.add_linked_fields(link_name='state', field_names=['position'])


class Component(BaseComponent):
    category: str = 'behavior_models'

    def __init__(self, data: VedoMemory):
        BaseComponent.__init__(self, data=data)

    def create(self) -> None:

        # Access Data fields
        positions = self.data.get_data(link_name='state', field_name='position')
        indices = self.data.get_data(field_name='indices')

        # Create the Vedo Actor
        self.vedo_object = Glyph(mesh=positions[indices],
                                 glyph=Box(size=[0.15]*3),
                                 alpha=STYLES[self.category]['alpha'],
                                 c=STYLES[self.category]['color'])

    def update(self, idx: Optional[int] = None) -> None:

        pass

    def read_memory(self) -> None:

        pass
