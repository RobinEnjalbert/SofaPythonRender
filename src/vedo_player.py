from typing import Optional, Callable
from os.path import join, dirname
import Sofa
from vedo import Plotter, Text2D
from time import time

from SofaRender.render.scene_factory import SceneFactory


class VedoPlayer(Plotter):
    PLAY_SYMBOL = "  \u23F5  "
    PAUSE_SYMBOL = "  \u23F8  "
    ONE_BACK_SYMBOL = " \u29CF "
    ONE_FORWARD_SYMBOL = " \u29D0 "

    def __init__(self,
                 root_node: Sofa.Core.Node,
                 step_function: Optional[Callable] = None,
                 **kwargs):

        Plotter.__init__(self, bg=join(dirname(__file__), 'data', 'back.png'), interactive=True, **kwargs)

        # Add the objects from the SOFA scene
        self.root = root_node
        self.factory = SceneFactory(self.root)
        self.factory.create_models()
        self.add(*self.factory.get_models())

        # Add the widgets
        self.__animate = True
        self.play_pause_btn = self.add_button(fnc=self.toggle, pos=[0.5, 0.05],
                                              states=[self.PAUSE_SYMBOL, self.PLAY_SYMBOL],
                                              font='Kanopus', bc=['red4', 'green3'])
        self.backward_btn = self.add_button(fnc=self.one_backward, pos=[0.44, 0.05],
                                            states=[self.ONE_BACK_SYMBOL],
                                            font='Kanopus', bc='green3', c='w')
        self.forward_btn = self.add_button(fnc=self.one_forward, pos=[0.56, 0.05],
                                           states=[self.ONE_FORWARD_SYMBOL],
                                           font='Kanopus', bc='green3', c='w')
        self.text = Text2D(txt='FPS:  0\nTime: 0\nStep: 0', font='Glasgo', s=0.75)
        self.add(self.text)
        self.__fps = 0
        self.__id_frame = 0
        self.__nb_frame = 0

        # Create the timer callback
        self.__step_fct = self.__default_step_function() if step_function is None else step_function
        self.add_callback(event_name='timer', func=self.step, enable_picking=False)
        self.timer_id = self.timer_callback('create')

        # Update the background
        self.render()
        self.background_renderer.GetActiveCamera().Zoom(2)

    def __default_step_function(self) -> Callable:
        def step_function():
            Sofa.Simulation.animate(self.root, self.root.dt.value)
        return step_function

    def step(self, _):
        t = time()
        self.__step_fct()
        self.factory.update_models(plt=self)
        self.__fps = round(0.9 * self.__fps + 0.1 / (time() - t), 1)
        self.__nb_frame = int(self.root.time.value / self.root.dt.value)
        self.text.text(f'FPS:  {self.__fps}\n'
                       f'Time: {round(self.root.time.value, 3)}\n'
                       f'Step: {self.__nb_frame}')
        self.render()

    def set_frame(self, idx: int):
        t = time()
        self.factory.update_models(plt=self, idx=idx)
        self.__fps = round(0.9 * self.__fps + 0.1 / (time() - t), 1)
        self.text.text(f'FPS:  {self.__fps}\n'
                       f'Time: {round(self.root.time.value, 3)}\n'
                       f'Step: {int(self.root.time.value / self.root.dt.value)}')
        self.render()

    def pause(self):
        self.__animate = False
        if self.timer_id is not None:
            self.timer_callback(action='destroy', timer_id=self.timer_id)
            self.timer_id = None
            self.__id_frame = self.__nb_frame
        self.play_pause_btn.status(self.PLAY_SYMBOL)

    def resume(self):
        self.__animate = True
        if self.timer_id is not None:
            self.timer_callback(action='destroy', timer_id=self.timer_id)
        self.timer_id = self.timer_callback(action='create')
        self.play_pause_btn.status(self.PAUSE_SYMBOL)

    def toggle(self, obj, evt):
        if self.__animate:
            self.pause()
        else:
            self.resume()

    def one_forward(self, obj, evt):
        if not self.__animate:
            self.__id_frame += 1

            if self.__id_frame > self.__nb_frame:
                self.step(None)
            else:
                self.set_frame(idx=self.__id_frame)

    def one_backward(self, obj, evt):
        if not self.__animate:
            self.__id_frame = max(0, self.__id_frame - 1)
            self.set_frame(idx=self.__id_frame)
