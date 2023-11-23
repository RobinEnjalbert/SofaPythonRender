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
                 step_function: Optional[Callable] = None):
        """
        Vedo-based visualizer for SOFA scenes.

        :param root_node: Root node of the SOFA scene graph.
        :param step_function: Timer callback function to execute. Default is a call to Sofa.Simulation.animate().
        """

        Plotter.__init__(self, bg=join(dirname(__file__), 'data', 'back.png'), interactive=True)

        # Add to the Plotter the objects from the SOFA scene with a SceneFactory
        self.root = root_node
        self.factory = SceneFactory(self.root)
        self.factory.create_models()
        self.add(*self.factory.get_models())

        # Add to the Plotter the required widgets
        self.__animate = True
        self.play_pause_btn = self.add_button(fnc=self.__toggle, pos=[0.5, 0.05],
                                              states=[self.PAUSE_SYMBOL, self.PLAY_SYMBOL],
                                              font='Kanopus', bc=['red4', 'green3'])
        self.backward_btn = self.add_button(fnc=self.__one_backward, pos=[0.44, 0.05],
                                            states=[self.ONE_BACK_SYMBOL],
                                            font='Kanopus', bc='green3', c='w')
        self.forward_btn = self.add_button(fnc=self.__one_forward, pos=[0.56, 0.05],
                                           states=[self.ONE_FORWARD_SYMBOL],
                                           font='Kanopus', bc='green3', c='w')
        self.slider = None

        # Add to the Plotter Text information about the simulation status
        self.text = Text2D(txt='FPS:  0\nTime: 0\nStep: 0', font='Glasgo', s=0.75)
        self.add(self.text)
        self.__fps = 0
        self.__id_frame = 0
        self.__nb_frame = 0

        # Create the timer callback
        self.__time_step_fct = self.__default_step_function() if step_function is None else step_function
        self.add_callback(event_name='timer', func=self.step, enable_picking=False)
        self.timer_id = self.timer_callback('create')

        # Update the background to have a SOFA-like look
        self.render()
        self.background_renderer.GetActiveCamera().Zoom(2)

    def __default_step_function(self) -> Callable:
        """
        Create the default time step function of the root node.
        :return: Sofa.Simulation.animate(root)
        """

        def step_function():
            Sofa.Simulation.animate(self.root, self.root.dt.value)
        return step_function

    def step(self, evt) -> None:
        """
        Timer callback of the viewer.
        """

        # Launch the user time step function and update the vedo objects
        t = time()
        self.__time_step_fct()
        self.factory.update_models(plt=self)
        self.__fps = round(0.9 * self.__fps + 0.1 / (time() - t), 1)

        # Update the simulation status
        self.__nb_frame = round(self.root.time.value / self.root.dt.value)
        self.text.text(f'FPS:  {self.__fps}\n'
                       f'Time: {round(self.root.time.value, 3)}\n'
                       f'Step: {self.__nb_frame}')
        self.render()

    def set_frame(self, idx: int) -> None:
        """
        Select a previously computed frame.

        :param idx: Index of the frame.
        """

        # Update the vedo objects
        t = time()
        self.factory.update_models(plt=self, idx=idx)
        self.__fps = round(0.9 * self.__fps + 0.1 / (time() - t), 1)

        # Update the simulation status
        self.text.text(f'FPS:  {self.__fps}\n'
                       f'Time: {round(self.__id_frame * self.root.dt.value, 3)}\n'
                       f'Step: {self.__id_frame}')
        self.render()

    def __pause(self):
        """

        :return:
        """

        self.__animate = False
        if self.timer_id is not None:
            self.timer_callback(action='destroy', timer_id=self.timer_id)
            self.timer_id = None
            self.__id_frame = self.__nb_frame
        self.play_pause_btn.status(self.PLAY_SYMBOL)
        if self.slider is None:
            self.slider = self.add_slider(sliderfunc=self.__slider_callback,
                                          xmin=0, xmax=self.__nb_frame, value=self.__id_frame,
                                          pos=[[0.25, 0.06], [0.75, 0.06]], show_value=False, c='grey3')

    def __resume(self):
        self.__animate = True
        if self.timer_id is not None:
            self.timer_callback(action='destroy', timer_id=self.timer_id)
        self.timer_id = self.timer_callback(action='create')
        self.play_pause_btn.status(self.PAUSE_SYMBOL)
        if self.slider is not None:
            self.sliders = []
            self.slider = None

    def __toggle(self, obj, evt):
        if self.__animate:
            self.__pause()
        else:
            self.__resume()

    def __one_forward(self, obj, evt):
        if not self.__animate:
            self.__id_frame += 1

            if self.__id_frame > self.__nb_frame:
                self.step(None)
                self.sliders = []
                self.slider = self.add_slider(sliderfunc=self.__slider_callback,
                                              xmin=0, xmax=self.__nb_frame, value=self.__id_frame,
                                              pos=[[0.25, 0.06], [0.75, 0.06]], show_value=False, c='grey3')
            else:
                self.set_frame(idx=self.__id_frame)
                self.slider.value = self.__id_frame

    def __one_backward(self, obj, evt):
        if not self.__animate:
            self.__id_frame = max(0, self.__id_frame - 1)
            self.set_frame(idx=self.__id_frame)
            self.slider.value = self.__id_frame

    def __slider_callback(self, obj, evt):
        self.__id_frame = round(obj.value)
        self.set_frame(idx=self.__id_frame)
