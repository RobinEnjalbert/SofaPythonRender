from typing import Dict, Type
from os import listdir
from os.path import dirname
from importlib import import_module

from SofaRender.render.components.Base import BaseConfig, BaseComponent


CONFIGS: Dict[str, BaseConfig] = {}
COMPONENTS: Dict[str, Type[BaseComponent]] = {}
exceptions = ['__init__.py', 'Base.py']
for mod in [m.split('.')[0] for m in listdir(dirname(__file__)) if m.endswith('.py') and m not in exceptions]:
    CONFIGS[mod] = getattr(import_module(f'SofaRender.render.components.{mod}'), 'Config')()
    COMPONENTS[mod] = getattr(import_module(f'SofaRender.render.components.{mod}'), 'Component')
