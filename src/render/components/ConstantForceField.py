from typing import Dict, Optional
import Sofa
from vedo import Arrows, Plotter

from SofaRender.render.components.Base import BaseComponent
from SofaRender.render.settings import STYLES


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
        self.vedo_object = Arrows(start_pts=start_position,
                                  end_pts=end_position,
                                  c=color,
                                  alpha=alpha)

    def update(self, plt: Plotter, idx: Optional[int] = None) -> None:

        # Access Data fields
        if idx is None:
            positions = self.attached_MO.position.value[self.sofa_object.indices.value]
            forces = self.sofa_object.forces.value
            self.store(positions=positions, forces=forces)
        else:
            frame = self.get_item(idx=idx)
            positions = frame['positions']
            forces = frame['forces']

        # Update the Vedo Actor
        plt.remove(self.vedo_object)
        end_positions = positions + forces * self.sofa_object.showArrowSize.value
        color = STYLES[self.category]['color']
        alpha = STYLES[self.category]['alpha']
        self.vedo_object = Arrows(start_pts=positions,
                                  end_pts=end_positions,
                                  c=color,
                                  alpha=alpha)
        plt.add(self.vedo_object)
