from typing import Optional, Dict
import Sofa
from vedo import BaseActor, Plotter


STYLES = {'visual_models':    {'color': 'green5',  'alpha': 1.},
          'collision_models': {'color': 'orange5', 'alpha': 1.},
          'behavior_models':  {'color': 'red6',    'alpha': 0.9},
          'force_fields':     {'color': 'green5',  'alpha': 1.}}


class BaseComponent:
    category: str = ''

    def __init__(self, sofa_object: Sofa.Core.Object, context: Dict[str, Sofa.Core.Object]):

        self.sofa_object: Sofa.Core.Object = sofa_object
        self.vedo_actor: Optional[BaseActor] = None

    def update(self, plt: Plotter) -> None:
        raise NotImplementedError
