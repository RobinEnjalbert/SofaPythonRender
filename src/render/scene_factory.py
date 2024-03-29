from typing import Dict, List, Optional
import Sofa
from vedo import Points, Plotter

from SofaRender.graph import SofaGraph
from SofaRender.render.components import BaseComponent, COMPONENTS


class SceneFactory:

    def __init__(self, root_node: Sofa.Core.Node):

        self.__graph = SofaGraph(root_node)
        self.display_models: Dict[str, bool] = {'visual_models': True,
                                                'collision_models': False,
                                                'behavior_models': False,
                                                'force_fields': False}
        self.__models: Dict[str, List[BaseComponent]] = {}
        self.create_models()

    def create_models(self):

        for key, sofa_object in self.__graph.graph.items():
            # Key format: root.child1.child2.@.Component<name>
            component_name = key.split('@.')[1].split('<')[0]
            if component_name in COMPONENTS:
                component = COMPONENTS[component_name]
                if component.category not in self.__models:
                    self.__models[component.category] = []
                context = self.__graph.graph[f'{key.split("@")[0]}@']
                self.__models[component.category].append(component(sofa_object=sofa_object, context=context))
            elif component_name == 'VisualStyle':
                flags = sofa_object.displayFlags.value.split(' ')
                for flag in flags:
                    display = flag[:4] == 'show'
                    for model in self.display_models.keys():
                        if model.split('_')[0] in flag[4:].lower():
                            self.display_models[model] = display
                            break

    def get_models(self) -> List[Points]:

        models = []
        for model_name, model_list in self.__models.items():
            if self.display_models[model_name]:
                models += [model.vedo_object for model in model_list]
        return models

    def update_models(self, plt: Plotter, idx: Optional[int] = None) -> None:

        for model_name, model_list in self.__models.items():
            if self.display_models[model_name]:
                for model in model_list:
                    model.update(plt=plt, idx=idx)
