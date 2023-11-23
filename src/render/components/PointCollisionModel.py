from typing import Dict, Optional
import Sofa
from vedo import Points, Plotter

from SofaRender.render.components.Base import BaseComponent
from SofaRender.render.settings import STYLES


class PointCollisionModel(BaseComponent):
    category: str = 'collision_models'

    def __init__(self, sofa_object: Sofa.Core.Object, context: Dict[str, Sofa.Core.Object]):
        BaseComponent.__init__(self, sofa_object, context)

        # Access Data fields
        context = {key.split('<')[0]: value for key, value in context.items()}
        self.attached_MO = context['MechanicalObject']
        positions = self.attached_MO.position.value
        self.store(positions=positions.copy())
        color = STYLES[self.category]['color']
        alpha = STYLES[self.category]['alpha']

        # Create the Vedo Actor
        self.vedo_object = Points(inputobj=positions,
                                  r=7,
                                  c=color,
                                  alpha=alpha)

    def update(self, plt: Plotter, idx: Optional[int] = None) -> None:

        # Access Data fields
        if idx is None:
            positions = self.attached_MO.position.value
            self.store(positions=positions.copy())
        else:
            positions = self.get_item(idx=idx)['positions']

        # Update the Vedo Actor
        self.vedo_object.vertices = positions
