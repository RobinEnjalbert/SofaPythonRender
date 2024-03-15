from os.path import join, dirname
from vedo import Plotter, Cube
import numpy as np

from SofaRender.render.remote.vedo_factory import VedoFactory


PLAY_SYMBOL = "  \u23F5  "
PAUSE_SYMBOL = "  \u23F8  "
ONE_BACK_SYMBOL = " \u29CF "
ONE_FORWARD_SYMBOL = " \u29D0 "


class VedoViewer(Plotter):

    def __init__(self, port_nb: int):

        super().__init__(bg=join(dirname(__file__), 'back.png'), interactive=True)

        self.factory = VedoFactory(port=port_nb)
        self.add(*self.factory.get_objects())

        # Timer callback
        self.add_callback('timer', func=self.__callback)
        self.timer_callback('create')

        # self.cube = Cube()
        # self.add(self.cube)

        # Update the background to have a SOFA-like look
        self.render()
        self.background_renderer.GetActiveCamera().Zoom(2)
        self.show(axes=4).close()

    def __callback(self, _):

        # self.cube.vertices += 0.01 * np.random.uniform(-1, 1, self.cube.vertices.shape)
        self.render(resetcam=False)


if __name__ == '__main__':

    from sys import argv
    VedoViewer(port_nb=int(argv[1]))
