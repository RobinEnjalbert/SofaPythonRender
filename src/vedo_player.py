from typing import Optional, Callable
from os.path import join, dirname
import Sofa
from vedo import Plotter
from vedo.applications import AnimationPlayer

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
        self.add_callback(event_name='timer', func=self.step, enable_picking=False)
        self.timer_id = self.timer_callback('create')

        self.render()
        self.background_renderer.GetActiveCamera().Zoom(2)

        self.__animate = True
        self.play_pause_btn = self.add_button(fnc=self.toggle,
                                              pos=[0.5, 0.05],
                                              states=[AnimationPlayer.PAUSE_SYMBOL, AnimationPlayer.PLAY_SYMBOL],
                                              font='Kanopus',
                                              bc=['red4', 'green3'])

    def __default_step_function(self) -> Callable:
        def step_function():
            Sofa.Simulation.animate(self.root, self.root.dt.value)
        return step_function

    def step(self, _):
        self.__step_fct()
        self.factory.update_models(self)
        self.render()

    def pause(self):
        self.__animate = False
        if self.timer_id is not None:
            self.timer_callback(action='destroy', timer_id=self.timer_id)
            self.timer_id = None
        self.play_pause_btn.status(AnimationPlayer.PLAY_SYMBOL)

    def resume(self):
        self.__animate = True
        if self.timer_id is not None:
            self.timer_callback(action='destroy', timer_id=self.timer_id)
        self.timer_id = self.timer_callback(action='create')
        self.play_pause_btn.status(AnimationPlayer.PAUSE_SYMBOL)

    def toggle(self, obj, evt):
        if self.__animate:
            self.pause()
        else:
            self.resume()
