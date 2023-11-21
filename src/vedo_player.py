from typing import Optional, Callable
from os.path import join, dirname
import Sofa
from vedo import Plotter

from SofaRender.render.scene_factory import SceneFactory


class VedoPlayer(Plotter):

    def __init__(self,
                 root_node: Sofa.Core.Node,
                 step_function: Optional[Callable] = None,
                 **kwargs):

        Plotter.__init__(self, bg=join(dirname(__file__), 'data', 'back.png'), interactive=True, **kwargs)

        self.root = root_node
        self.factory = SceneFactory(self.root)
        self.factory.create_models()
        self.add(*self.factory.get_models())

        self.__step_fct = self.__default_step_function() if step_function is None else step_function
        self.add_callback('timer', self.step)
        self.timer_callback('create')

        self.render()
        self.background_renderer.GetActiveCamera().Zoom(2)

    def __default_step_function(self) -> Callable:
        def step_function():
            Sofa.Simulation.animate(self.root, self.root.dt.value)
        return step_function

    def step(self, _):
        self.__step_fct()
        self.factory.update_models(self)
        self.render()
