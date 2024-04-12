from os.path import join, dirname
from vedo import Plotter, Text2D
from time import time

from SofaRender.render.remote.vedo_factory import VedoFactory


PLAY_SYMBOL = "  \u23F5  "
PAUSE_SYMBOL = "  \u23F8  "
BACKWARD_SYMBOL = " \u29CF "
FORWARD_SYMBOL = " \u29D0 "


class VedoViewer(Plotter):

    def __init__(self,
                 port_nb: int,
                 animation_player: bool):

        super().__init__(bg=join(dirname(__file__), 'back.png'), interactive=True)

        self.factory = VedoFactory(port=port_nb, plt=self, store_data=animation_player)
        self.add(*self.factory.get_objects())

        # Add animation widgets
        if animation_player:
            self.__animate = True
            self.play_button = self.add_button(fnc=self.__toggle, pos=[0.5, 0.05], font='Kanopus',
                                               states=[PAUSE_SYMBOL, PLAY_SYMBOL], bc=['red4', 'green3'])
            self.backward_button = self.add_button(fnc=self.__backward, pos=[0.44, 0.05], font='Kanopus',
                                                   states=[BACKWARD_SYMBOL], bc='green3', c='white')
            self.forward_button = self.add_button(fnc=self.__forward, pos=[0.56, 0.05], font='Kanopus',
                                                  states=[FORWARD_SYMBOL], bc='green3', c='white')
            self.slider = None
            # self.add_callback()

            # Add text information about the simulation status
            self.text = Text2D(txt='FPS:  0\nTime: 0\nStep: 0', font='Glasgo', s=0.75)
            self.add(self.text)
            self.__fps, self.__id_frame = 0, 0
            self.__root_times = [0.]

        # Timer callback
        self.add_callback(event_name='timer', func=self.__callback_animation if animation_player else self.__callback,
                          enable_picking=not animation_player)
        self.timer_id = self.timer_callback('create', dt=1)
        self.step_idx = 0

        # Update the background to have a SOFA-like look
        self.render()
        self.background_renderer.GetActiveCamera().Zoom(2)

        self.factory.start()
        self.__time = time()
        self.show(axes=4).close()

        if animation_player:
            self.__animate = True

    @property
    def is_blocked(self) -> bool:
        return not self.__animate

    def __callback(self, _):

        if self.step_idx < self.factory.step_idx:
            self.factory.update()
            self.step_idx += 1
        self.render(resetcam=False)

    def __callback_animation(self, _):

        if self.step_idx < self.factory.step_idx:
            self.factory.update()
            t = time()
            self.__fps = round(0.9 * self.__fps + 0.1 / (t - self.__time), 1)
            self.__time = t
            self.step_idx += 1
            self.__root_times.append(round(self.step_idx * self.factory.root_time[0], 2))
            self.text.text(txt=f'FPS:   {self.__fps}\nTime: {self.__root_times[-1]}\nStep: {self.step_idx}')
        self.render(resetcam=False)

    def __toggle(self, obj, evt):

        self.play_button.switch()
        if self.__animate:
            self.__pause()
        else:
            self.__play()

    def __pause(self):

        self.__animate = False
        if self.timer_id is not None:
            self.timer_callback(action='destroy', timer_id=self.timer_id)
            self.timer_id = None
            self.__id_frame = self.step_idx
        if self.slider is None:
            self.slider = self.add_slider(sliderfunc=self.__select_frame, pos=[[0.25, 0.06], [0.75, 0.06]], c='grey3',
                                          xmin=0, xmax=self.__id_frame, value=self.__id_frame, show_value=False)

    def __play(self):

        self.__animate = True
        if self.timer_id is not None:
            self.timer_callback(action='destroy', timer_id=self.timer_id)
        self.timer_id = self.timer_callback(action='create')
        self.__time = time()
        if self.slider is not None:
            self.slider = None
            self.sliders = []

    def __backward(self, obj, evt):

        if not self.__animate:
            self.__id_frame = max(0, self.__id_frame - 1)
            self.__set_frame(idx=self.__id_frame)
            self.slider.value = self.__id_frame

    def __forward(self, obj, evt):

        if not self.__animate:
            self.__id_frame = min(self.__id_frame + 1, self.step_idx)
            self.__set_frame(idx=self.__id_frame)
            self.slider.value = self.__id_frame

    def __select_frame(self, obj, evt):

        self.__id_frame = round(obj.value)
        self.__set_frame(idx=self.__id_frame)

    def __set_frame(self, idx: int):

        # Update the vedo objects
        self.factory.set_frame(idx=idx)
        self.text.text(txt=f'FPS:   {self.__fps}\nTime: {self.__root_times[self.__id_frame]}\nStep: {self.__id_frame}')
        self.render()


if __name__ == '__main__':

    from sys import argv
    VedoViewer(port_nb=int(argv[1]),
               animation_player=argv[2] == 'True')
