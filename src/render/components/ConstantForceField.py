from typing import Optional
from vedo import Arrows, plotter_instance

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
        positions = self.data.get_data(link_name='state', field_name='position')[0]
        positions = positions[self.data.get_data(field_name='indices')[0]]
        forces = self.data.get_data(field_name='forces')[0]
        size = self.data.get_data(field_name='showArrowSize')[0]

        # Store data
        # self.store(positions=positions, forces=forces, size=size)
        self.dirty_flags = {'positions': False, 'indices': False, 'forces': False, 'size': False}

        # Create the Vedo Actor
        self.vedo_object = Arrows(start_pts=positions,
                                  end_pts=positions + forces * size,
                                  c=STYLES[self.category]['color'],
                                  alpha=STYLES[self.category]['alpha'])

    def update(self, idx: Optional[int] = None) -> None:

        pass

        # if True in self.dirty_flags.values():
        #
        #     # Access Data fields
        #     frame = self.get_item(idx=idx)
        #     positions, forces, size = frame['positions'], frame['forces'], frame['size']
        #
        #     # Update the Vedo Actor
        #     # Todo: see how to update Arrows instead of remove/add
        #     plotter_instance.remove(self.vedo_object)
        #     self.vedo_object = Arrows(start_pts=positions,
        #                               end_pts=positions + forces * size,
        #                               c=STYLES[self.category]['color'],
        #                               alpha=STYLES[self.category]['alpha'])
        #     plotter_instance.add(self.vedo_object)

    def read_memory(self) -> None:

        pass

        # positions, dirty_p = self.data.update_data(link_name='state', field_name='position')
        # indices, dirty_i = self.data.update_data(field_name='indices')
        # forces, dirty_f = self.data.update_data(field_name='forces')
        # size, dirty_s = self.data.update_data(field_name='showArrowSize')
        # self.store(positions=positions[indices], forces=forces, size=size)
        # self.dirty_flags = {'positions': dirty_p, 'indices': dirty_i, 'forces': dirty_f, 'size': dirty_s}
