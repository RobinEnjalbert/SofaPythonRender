from typing import Optional
from vedo import Mesh

from SofaRender.render.components.Base import BaseConfig, BaseComponent
from SofaRender.render.remote.vedo_memory import VedoMemory
from SofaRender.render.settings import STYLES


class Config(BaseConfig):

    def __init__(self):
        super().__init__()
        self.add_object_fields(['position', 'triangles', 'quads', 'material', 'texturename', 'texcoords'])


class Component(BaseComponent):
    category: str = 'visual_models'

    def __init__(self, data: VedoMemory):
        BaseComponent.__init__(self, data=data)

    def create(self) -> None:

        # Access Data fields
        positions = self.data.get_data(field_name='position')
        topology = []
        for topo_type in ('triangles', 'quads'):
            if (topo := self.data.get_data(field_name=topo_type)) is not None:
                topology += topo.tolist()
        colors = self.data.get_data(field_name='material').item()
        colors = colors.split('Diffuse')[1].split('Ambient')[0].split(' ')[2:-1]
        alpha = max(0.1, float(colors[-1]))
        texture = self.data.get_data(field_name='texturename').item()
        texcoords = self.data.get_data(field_name='texcoords')

        # Store Data
        self.store(positions=positions, alpha=alpha)
        self.dirty_flags = {'positions': False, 'colors': False}

        # Create the Vedo Actor
        self.vedo_object = Mesh(inputobj=[positions, topology],
                                c=[float(c) for c in colors[:-1]],
                                alpha=alpha)
        if texture != '':
            self.vedo_object.texture(texture, tcoords=texcoords)

    def update(self, idx: Optional[int] = None) -> None:

        pass

        # # Access Data fields
        # data = self.get_item(idx=idx)
        # positions = data['positions']
        # alpha = data['alpha']
        #
        # # Update the Vedo Actor
        # if self.dirty_flags['positions']:
        #     self.vedo_object.vertices = positions
        # if self.dirty_flags['colors']:
        #     self.vedo_object.alpha(alpha)

    def read_memory(self) -> None:

        pass

        # positions, dirty_p = self.data.update_data(field_name='position')
        # colors, dirty_c = self.data.update_data(field_name='material')
        # colors = colors.item().split('Diffuse')[1].split('Ambient')[0].split(' ')[2:-1]
        # alpha = max(0.1, float(colors[-1]))
        # self.store(positions=positions, alpha=alpha)
        # self.dirty_flags = {'positions': dirty_p, 'colors': dirty_c}
