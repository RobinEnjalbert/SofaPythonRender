from typing import Optional
from vedo import Mesh, Plotter, show

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
        colors = self.data.get_data(field_name='material').item().split('Diffuse')[1].split('Ambient')[0].split(' ')[2:-1]
        alpha = max(0.1, float(colors[-1]))
        texture = self.data.get_data(field_name='texturename').item()
        texcoords = self.data.get_data(field_name='texcoords')
        self.store(positions=positions, alpha=alpha)

        # Create the Vedo Actor
        self.vedo_object = Mesh(inputobj=[positions, topology],
                                c=[float(c) for c in colors[:-1]],
                                alpha=alpha)

        if texture != '':
            self.vedo_object.texture(texture, tcoords=texcoords)

    def update(self, plt: Plotter, idx: Optional[int] = None) -> None:

        # Access Data fields
        if idx is None:
            positions = self.sofa_object.position.value
            colors = self.sofa_object.material.value.split('Diffuse')[1].split('Ambient')[0].split(' ')[2:-1]
            alpha = max(0.1, float(colors[-1])) if self.sofa_object.enable.value else 0.
            self.store(positions=positions.copy(), alpha=alpha)
        else:
            data = self.get_item(idx=idx)
            positions = data['positions']
            alpha = data['alpha']

        # Update the Vedo Actor
        self.vedo_object.vertices = positions
        self.vedo_object.alpha(alpha)
