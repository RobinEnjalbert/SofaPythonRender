from os.path import join, dirname
from vedo import Plotter

from SofaRender.render.remote.vedo_factory import VedoFactory


PLAY_SYMBOL = "  \u23F5  "
PAUSE_SYMBOL = "  \u23F8  "
ONE_BACK_SYMBOL = " \u29CF "
ONE_FORWARD_SYMBOL = " \u29D0 "


class VedoViewer(Plotter):

    def __init__(self,
                 port_nb: int,
                 animation_player: bool):

        super().__init__(bg=join(dirname(__file__), 'back.png'), interactive=True)

        self.factory = VedoFactory(port=port_nb, plt=self)
        self.add(*self.factory.get_objects())

        # Timer callback
        self.add_callback('timer', func=self.__callback)
        self.timer_callback('create', dt=1)
        self.step_idx = 0

        # Update the background to have a SOFA-like look
        self.render()
        self.background_renderer.GetActiveCamera().Zoom(2)

        self.factory.start()
        self.show(axes=4).close()

    def __callback(self, _):

        if self.step_idx < self.factory.step_idx:
            self.step_idx += 1
            self.factory.update_models(idx=self.step_idx)
        self.render(resetcam=False)


if __name__ == '__main__':

    from sys import argv
    VedoViewer(port_nb=int(argv[1]),
               animation_player=argv[2] == 'True')
