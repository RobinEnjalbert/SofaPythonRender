from typing import Dict, Optional
import Sofa
from vedo import Glyph, Box, Plotter

from SofaRender.render.components.Base import BaseComponent
from SofaRender.render.settings import STYLES


class FixedConstraint(BaseComponent):
    category: str = 'behavior_models'

    def __init__(self, sofa_object: Sofa.Core.Object, context: Dict[str, Sofa.Core.Object]):
        BaseComponent.__init__(self, sofa_object, context)

        # Access Data fields
        context = {key.split('<')[0]: value for key, value in context.items()}
        self.attached_MO = context['MechanicalObject']
        positions = self.attached_MO.position.value
        indices = self.sofa_object.indices.value
        color = STYLES[self.category]['color']
        alpha = STYLES[self.category]['alpha']

        # Create the Vedo Actor
        self.vedo_object = Glyph(mesh=positions[indices],
                                 glyph=Box(size=[0.15]*3),
                                 alpha=alpha,
                                 c=color)

    def update(self, plt: Plotter, idx: Optional[int] = None) -> None:
        pass
