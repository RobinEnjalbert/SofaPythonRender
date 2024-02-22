from typing import Optional, Callable
from os.path import join, dirname
import Sofa
from vedo import Plotter, Text2D
from time import time


class VedoViewer(Plotter):
    PLAY_SYMBOL = "  \u23F5  "
    PAUSE_SYMBOL = "  \u23F8  "

    def __init__(self,
                 root_node: Sofa.Core.Node,
                 step_function: Optional[Callable] = None):

        Plotter.__init__(self, bg=join(dirname(__file__), 'data', 'back.png'), interactive=True)

        self.root = root_node

        # Add animation widgets
        self.__animate = True
        self.play_pause_btn = self.add_button(fnc=self.__toggle, pos=[0.5, 0.05],
                                              states=[self.PAUSE_SYMBOL, self.PLAY_SYMBOL],
                                              font='Kanopus', bc=['red4', 'green3'])

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

        # Update the background to have a Sofa-like look
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
        self.__fps = round(0.9 * self.__fps + 0.1 / (time() - t), 1)

        # Update the simulation status
        self.__nb_frame = round(self.root.time.value / self.root.dt.value)
        self.text.text(f'FPS:  {self.__fps}\n'
                       f'Time: {round(self.root.time.value, 3)}\n'
                       f'Step: {self.__nb_frame}')
        self.render()

    def __toggle(self, obj, evt):
        if self.__animate:
            self.__pause()
        else:
            self.__resume()

    def __pause(self):
        self.__animate = False
        if self.timer_id is not None:
            self.timer_callback(action='destroy', timer_id=self.timer_id)
            self.timer_id = None
            self.__id_frame = self.__nb_frame
        self.play_pause_btn.status(self.PLAY_SYMBOL)

    def __resume(self):
        self.__animate = True
        if self.timer_id is not None:
            self.timer_callback(action='destroy', timer_id=self.timer_id)
        self.timer_id = self.timer_callback(action='create')
        self.play_pause_btn.status(self.PAUSE_SYMBOL)
