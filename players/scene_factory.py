from typing import Dict, Tuple, List
import Sofa
from vedo import Plotter, Mesh
from .sofa_graph import SofaGraph


class SceneFactory:

    def __init__(self, root_node: Sofa.Core.Node):

        self.graph = SofaGraph(root_node)
        self.__mesh_factory: Dict[str, Tuple[Mesh, Sofa.Core.Object]] = {}
        self.create_meshes()

    def create_meshes(self):

        for key, component in self.graph.graph.items():
            # Key format : root.child1.child2.@.Component<name>
            if key.split('@.')[1].split('<')[0] == 'OglModel':
                mesh = Mesh([component.position.value, component.triangles.value])
                colors = component.material.value.split('Diffuse')[1].split('Ambient')[0].split(' ')[2:-1]
                mesh.color([float(c) for c in colors[:-1]]).alpha(float(colors[-1]))
                self.__mesh_factory[key] = (mesh, component)

    def get_meshes(self) -> List[Mesh]:
        return [mesh[0] for mesh in self.__mesh_factory.values()]

    def update_meshes(self) -> None:
        for mesh, ogl_model in self.__mesh_factory.values():
            mesh.points(ogl_model.position.value)



