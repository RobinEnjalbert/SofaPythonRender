from typing import Optional, Dict
import Sofa
from vedo import Points, Plotter


class BaseComponent:
    category: str = ''

    def __init__(self, sofa_object: Sofa.Core.Object, context: Dict[str, Sofa.Core.Object]):

        self.sofa_object: Sofa.Core.Object = sofa_object
        self.vedo_object: Optional[Points] = None

    def update(self, plt: Plotter) -> None:
        raise NotImplementedError
