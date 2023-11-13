from typing import Dict
import Sofa
from vedo import Mesh, Plotter

from SofaRender.render.components.Base import BaseComponent


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

        # Create the Vedo Actor
        self.vedo_actor = Mesh(inputobj=[positions, triangles + quads],
                               c=[float(c) for c in colors[:-1]],
                               alpha=max(0.1, float(colors[-1])))
        if texture != '':
            self.vedo_actor.texture(texture, tcoords=texcoords)

    def update(self, plt: Plotter) -> None:

        # Access Data fields
        positions = self.sofa_object.position.value

        # Update the Vedo Actor
        self.vedo_actor.points(pts=positions)
