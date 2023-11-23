from typing import Dict, Optional
import Sofa
from vedo import Mesh, Plotter

from SofaRender.render.components.Base import BaseComponent
from SofaRender.render.settings import STYLES


class OglModel(BaseComponent):
    category: str = 'visual_models'

    def __init__(self, sofa_object: Sofa.Core.Object, context: Dict[str, Sofa.Core.Object]):
        BaseComponent.__init__(self, sofa_object, context)

        # Access Data fields
        positions = self.sofa_object.position.value
        triangles = list(self.sofa_object.triangles.value)
        quads = list(self.sofa_object.quads.value)
        colors = self.sofa_object.material.value.split('Diffuse')[1].split('Ambient')[0].split(' ')[2:-1]
        texture = self.sofa_object.texturename.value
        texcoords = self.sofa_object.texcoords.value
        self.store(positions=positions.copy())

        # Create the Vedo Actor
        self.vedo_object = Mesh(inputobj=[positions, triangles + quads],
                                c=[float(c) for c in colors[:-1]],
                                alpha=max(0.1, float(colors[-1])))
        if texture != '':
            self.vedo_object.texture(texture, tcoords=texcoords)

    def update(self, plt: Plotter, idx: Optional[int] = None) -> None:

        # Access Data fields
        if idx is None:
            positions = self.sofa_object.position.value
            self.store(positions=positions.copy())
        else:
            positions = self.get_item(idx=idx)['positions']

        # Update the Vedo Actor
        self.vedo_object.vertices = positions
