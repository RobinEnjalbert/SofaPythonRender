from typing import Dict, Optional
import Sofa
from vedo import Mesh, Plotter

from SofaRender.render.components.Base import BaseComponent
from SofaRender.render.settings import STYLES


class TriangleCollisionModel(BaseComponent):
    category: str = 'collision_models'

    def __init__(self, sofa_object: Sofa.Core.Object, context: Dict[str, Sofa.Core.Object]):
        BaseComponent.__init__(self, sofa_object, context)

        # Access Data fields
        context = {key.split('<')[0]: value for key, value in context.items()}
        self.attached_MO = context['MechanicalObject']
        positions = self.attached_MO.position.value
        triangles = self.sofa_object.topology.getLinkedBase().triangles.value
        self.store(positions=positions.copy())
        color = STYLES[self.category]['color']
        alpha = STYLES[self.category]['alpha']

        # Create the Vedo Actor
        self.vedo_object = Mesh(inputobj=[positions, triangles],
                                c=color, alpha=alpha).wireframe(True).lw(2)

    def update(self, plt: Plotter, idx: Optional[int] = None) -> None:

        # Access Data fields
        if idx is None:
            positions = self.sofa_object.position.value
            self.store(positions=positions.copy())
        else:
            positions = self.get_item(idx=idx)['positions']

        # Update the Vedo Actor
        self.vedo_object.vertices = positions
