from typing import Dict, Type
from os import listdir
from os.path import dirname

from SofaRender.render.components.Base import BaseComponent


COMPONENTS: Dict[str, Type[BaseComponent]] = {}
for mod in [m.split('.')[0] for m in listdir(dirname(__file__)) if m.endswith('.py') and m not in ['__init__.py', 'Base.py']]:
    COMPONENTS[mod] = getattr(__import__(f'SofaRender.render.components.{mod}', fromlist=[mod]), mod)
