from typing import Dict
import Sofa
from vedo import Mesh, Plotter

from SofaRender.render.components.Base import BaseComponent
from SofaRender.render.settings import STYLES


class LineCollisionModel(BaseComponent):
    category: str = 'collision_models'

    def __init__(self, sofa_object: Sofa.Core.Object, context: Dict[str, Sofa.Core.Object]):
        BaseComponent.__init__(self, sofa_object, context)

        # Access Data fields
        context = {key.split('<')[0]: value for key, value in context.items()}
        self.attached_MO = context['MechanicalObject']
        positions = self.attached_MO.position.value
        edges = self.sofa_object.topology.getLinkedBase().edges.value
        color = STYLES[self.category]['color']
        alpha = STYLES[self.category]['alpha']

        # Create the Vedo Actor
        self.vedo_object = Mesh(inputobj=[positions, edges],
                                c=color,
                                alpha=alpha).wireframe(True).lw(2)

    def update(self, plt: Plotter) -> None:

        # Access Data fields
        positions = self.attached_MO.position.value

        # Update the Vedo Actor
        self.vedo_object.vertices = positions