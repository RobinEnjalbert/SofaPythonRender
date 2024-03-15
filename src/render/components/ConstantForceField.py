from typing import Optional
from vedo import Arrows, Plotter

from SofaRender.render.components.Base import BaseConfig, BaseComponent
from SofaRender.render.remote.vedo_memory import VedoMemory
from SofaRender.render.settings import STYLES


class Config(BaseConfig):

    def __init__(self):
        super().__init__()
        self.add_object_fields(field_names=['indices', 'forces', 'showArrowSize'])
        self.add_linked_fields(link_name='state', field_names=['position'])


class Component(BaseComponent):
    category: str = 'force_fields'

    def __init__(self, data: VedoMemory):
        BaseComponent.__init__(self, data=data)

    def create(self) -> None:

        # Access Data fields
        positions = self.data.get_data(link_name='state', field_name='position')
        positions = positions[self.data.get_data(field_name='indices')]
        forces = self.data.get_data(field_name='forces')
        self.store(positions=positions, forces=forces)
        end_positions = positions + forces * self.data.get_data(field_name='showArrowSize')
        color = STYLES[self.category]['color']
        alpha = STYLES[self.category]['alpha']

        # Create the Vedo Actor
        self.vedo_object = Arrows(start_pts=positions,
                                  end_pts=end_positions,
                                  c=color,
                                  alpha=alpha)

    def update(self, plt: Plotter, idx: Optional[int] = None) -> None:

        # Access Data fields
        if idx is None:
            positions = self.attached_MO.position.value[self.sofa_object.indices.value]
            forces = self.sofa_object.forces.value
            self.store(positions=positions.copy(), forces=forces.copy())
        else:
            frame = self.get_item(idx=idx)
            positions = frame['positions']
            forces = frame['forces']

        # Update the Vedo Actor
        plt.remove(self.vedo_object)
        end_positions = positions + forces * self.sofa_object.showArrowSize.value
        color = STYLES[self.category]['color']
        alpha = STYLES[self.category]['alpha']
        self.vedo_object = Arrows(start_pts=positions,
                                  end_pts=end_positions,
                                  c=color,
                                  alpha=alpha)
        plt.add(self.vedo_object)
