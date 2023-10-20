from typing import Optional, Dict
import Sofa
from vedo import BaseActor


class BaseComponent:
    category: str = ''

    def __init__(self, sofa_object: Sofa.Core.Object, context: Dict[str, Sofa.Core.Object]):

        self.sofa_object: Sofa.Core.Object = sofa_object
        self.vedo_actor: Optional[BaseActor] = None

    def update(self) -> None:
        raise NotImplementedError
