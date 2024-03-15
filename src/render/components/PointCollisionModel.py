from typing import Optional
from vedo import Points, Plotter

from SofaRender.render.components.Base import BaseConfig, BaseComponent
from SofaRender.render.remote.vedo_memory import VedoMemory
from SofaRender.render.settings import STYLES


class Config(BaseConfig):

    def __init__(self):
        super().__init__()
        self.add_linked_fields(link_name='state', field_names=['position'])


class Component(BaseComponent):
    category: str = 'collision_models'

    def __init__(self, data: VedoMemory):
        BaseComponent.__init__(self, data=data)

    def create(self) -> None:

        # Access Data fields
        positions = self.data.get_data(link_name='state', field_name='position')
        self.store(positions=positions)
        color = STYLES[self.category]['color']
        alpha = STYLES[self.category]['alpha']

        # Create the Vedo Actor
        self.vedo_object = Points(inputobj=positions,
                                  r=7,
                                  c=color,
                                  alpha=alpha)

    def update(self, plt: Plotter, idx: Optional[int] = None) -> None:

        # Access Data fields
        if idx is None:
            positions = self.attached_MO.position.value
            self.store(positions=positions.copy())
        else:
            positions = self.get_item(idx=idx)['positions']

        # Update the Vedo Actor
        self.vedo_object.vertices = positions
