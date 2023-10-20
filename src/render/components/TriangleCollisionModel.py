from typing import Dict
import Sofa
from SofaRender.render.components.Base import BaseComponent
from vedo import Mesh


class TriangleCollisionModel(BaseComponent):
    category: str = 'collision_models'

    def __init__(self, sofa_object: Sofa.Core.Object, context: Dict[str, Sofa.Core.Object]):
        BaseComponent.__init__(self, sofa_object, context)

        # Access Data fields
        context = {key.split('<')[0]: value for key, value in context.items()}
        self.attached_MO = context['MechanicalObject']
        positions = self.attached_MO.position.value
        triangles = self.sofa_object.topology.getLinkedBase().triangles.value

        # Create the Vedo Actor
        self.vedo_actor = Mesh(inputobj=[positions, triangles],
                               c=[255, 130, 0]).wireframe(True).lw(2)

    def update(self) -> None:

        # Access Data fields
        positions = self.attached_MO.position.value

        # Update the Vedo Actor
        self.vedo_actor.points(pts=positions)
