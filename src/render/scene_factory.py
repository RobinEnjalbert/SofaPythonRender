from typing import Dict, List
import Sofa
from vedo import BaseActor

from SofaRender.graph import SofaGraph
from SofaRender.render.components import BaseComponent, COMPONENTS


class SceneFactory:

    def __init__(self, root_node: Sofa.Core.Node):

        self.__graph = SofaGraph(root_node)
        self.display_models: Dict[str, bool] = {}
        self.__models: Dict[str, List[BaseComponent]] = {}

    def create_models(self, visual_models: bool = True, collision_models: bool = True):

        self.display_models = locals()
        del self.display_models['self']

        for key, sofa_object in self.__graph.graph.items():
            # Key format: root.child1.child2.@.Component<name>
            component_name = key.split('@.')[1].split('<')[0]
            if component_name in COMPONENTS:
                component = COMPONENTS[component_name]
                if component.category not in self.__models:
                    self.__models[component.category] = []
                context = self.__graph.graph[f'{key.split("@")[0]}@']
                self.__models[component.category].append(component(sofa_object=sofa_object, context=context))

    def get_models(self) -> List[BaseActor]:

        models = []
        for model_name, model_list in self.__models.items():
            if self.display_models[model_name]:
                models += [model.vedo_actor for model in model_list]
        return models

    def update_models(self) -> None:

        for model_name, model_list in self.__models.items():
            if self.display_models[model_name]:
                for model in model_list:
                    model.update()
