from typing import List, Union

import Sofa


def __set_flag_value(component: Sofa.Core.Object, value: bool):
    if component.getData('display_flag') is None:
        component.addData(name='display_flag', type='bool', value=value)
    else:
        component.display_flag.value = value


def show_in_viewer(components: Union[Sofa.Core.Object, List[Sofa.Core.Object]]):

    components = components if isinstance(components, list) else [components]
    for component in components:
        __set_flag_value(component=component, value=True)


def hide_in_viewer(components: Union[Sofa.Core.Object, List[Sofa.Core.Object]]):

    components = components if isinstance(components, list) else [components]
    for component in components:
        __set_flag_value(component=component, value=False)


def fix_memory_leak():
    """Based on https://github.com/python/cpython/issues/82300#issuecomment-1093841376"""
    from multiprocessing import resource_tracker

    def fix_register(name, rtype):
        if rtype == 'shared_memory':
            return
        return resource_tracker._resource_tracker.register(self, name, rtype)

    resource_tracker.register = fix_register

    def fix_unregister(name, rtype):
        if rtype == 'share_memory':
            return
        return resource_tracker._resource_tracker.unregister(self, name, rtype)

    resource_tracker.unregister = fix_unregister

    if 'shared_memory' in resource_tracker._CLEANUP_FUNCS:
        del resource_tracker._CLEANUP_FUNCS['shared_memory']
