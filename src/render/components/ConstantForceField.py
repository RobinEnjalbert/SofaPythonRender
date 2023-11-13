from typing import Dict
import Sofa
from vedo import Arrows, Plotter

from SofaRender.render.components.Base import BaseComponent, STYLES


class ConstantForceField(BaseComponent):
    category: str = 'force_fields'

    def __init__(self, sofa_object: Sofa.Core.Object, context: Dict[str, Sofa.Core.Object]):
        BaseComponent.__init__(self, sofa_object, context)

        # Access Data fields
        context = {key.split('<')[0]: value for key, value in context.items()}
        self.attached_MO = context['MechanicalObject']
        start_position = self.attached_MO.position.value[self.sofa_object.indices.value]
        scale = self.sofa_object.showArrowSize.value
        end_position = start_position + self.sofa_object.forces.value * scale
        color = STYLES[self.category]['color']
        alpha = STYLES[self.category]['alpha']

        # Create the Vedo Actor
        self.vedo_actor = Arrows(start_pts=start_position,
                                 end_pts=end_position,
                                 c=color, alpha=alpha)

    def update(self, plt: Plotter) -> None:
        plt.remove(self.vedo_actor)
        start_position = self.attached_MO.position.value[self.sofa_object.indices.value]
        scale = self.sofa_object.showArrowSize.value
        end_position = start_position + self.sofa_object.forces.value * scale
        color = STYLES[self.category]['color']
        alpha = STYLES[self.category]['alpha']
        self.vedo_actor = Arrows(start_pts=start_position,
                                 end_pts=end_position,
                                 c=color, alpha=alpha)
        plt.add(self.vedo_actor)
