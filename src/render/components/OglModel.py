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
        positions, _ = self.data.get_data(field_name='position')
        topology = []
        for topo_type in ('triangles', 'quads'):
            topo, _ = self.data.get_data(field_name=topo_type)
            if topo is not None:
                topology += topo.tolist()
        colors = self.data.get_data(field_name='material')[0].item()
        colors = colors.split('Diffuse')[1].split('Ambient')[0].split(' ')[2:-1]
        alpha = max(0.1, float(colors[-1]))
        texture = self.data.get_data(field_name='texturename')[0].item()
        texcoords = self.data.get_data(field_name='texcoords')[0]

        # Create the Vedo Actor
        self.vedo_object = Mesh(inputobj=[positions, topology],
                                c=[float(c) for c in colors[:-1]],
                                alpha=alpha)
        if texture != '':
            self.vedo_object.texture(texture, tcoords=texcoords)

    def update(self, idx: Optional[int] = None) -> None:

        positions, dirty = self.data.get_data(field_name='position')
        if dirty:
            self.vedo_object.vertices = positions

        colors, dirty = self.data.get_data(field_name='material')
        if dirty:
            colors = colors.item().split('Diffuse')[1].split('Ambient')[0].split(' ')[2:-1]
            alpha = max(0.1, float(colors[-1]))
            self.vedo_object.alpha(alpha)
