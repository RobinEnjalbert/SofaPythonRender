from os.path import join, dirname
import Sofa
from vedo import Plotter

from SofaRender.render.scene_factory import SceneFactory


class VedoPlayer(Plotter):

    def __init__(self,
                 root_node: Sofa.Core.Node,
                 visual_models: bool = True,
                 collision_models: bool = True,
                 **kwargs):

        Plotter.__init__(self, bg=join(dirname(__file__), 'data', 'back.png'), interactive=True, **kwargs)

        self.render()
        self.background_renderer.GetActiveCamera().Zoom(2)

        self.root = root_node
        self.factory = SceneFactory(self.root)
        self.factory.create_models(visual_models=visual_models, collision_models=collision_models)
        self.add(*self.factory.get_models())

        self.add_callback('timer', self.step)
        self.timer_callback('create')

    def step(self, _):
        Sofa.Simulation.animate(self.root, self.root.dt.value)
        self.factory.update_models()
        self.render()
