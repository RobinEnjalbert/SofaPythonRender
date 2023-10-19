from os.path import join, dirname
import Sofa
from vedo import Plotter
from .scene_factory import SceneFactory


class VedoPlayer(Plotter):

    def __init__(self, root_node: Sofa.Core.Node, **kwargs):

        Plotter.__init__(self, bg=join(dirname(__file__), 'back.png'), interactive=True, **kwargs)
        self.render()
        self.background_renderer.GetActiveCamera().Zoom(2)
        self.root = root_node
        self.factory = SceneFactory(self.root)
        self.add(*self.factory.get_meshes())
        self.add_callback('timer', self.step)
        self.timer_callback('create')

    def step(self, _):
        Sofa.Simulation.animate(self.root, self.root.dt.value)
        self.factory.update_meshes()
        self.render()

