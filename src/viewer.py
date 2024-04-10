from typing import Optional
import Sofa
import threading
import subprocess
from sys import executable

from SofaRender.render.sofa_factory import SofaFactory
from SofaRender.render.remote import vedo_viewer


class Viewer:

    def __init__(self,
                 root_node: Sofa.Core.Node = None,
                 render_graph: bool = True,
                 animation_player: bool = False):
        """
        Vedo-based viewer for SOFA scenes.

        :param root_node: Root node of the SOFA scene graph.
        :param render_graph: If True, the scene graph will be explored to automatically create Vedo objects.
        :param animation_player: If True, adds play / pause buttons in the viewer to control the animation.
        """

        if not root_node.isInitialized():
            raise RuntimeError("You must call 'Sofa.Simulation.init(root_node)' before creating the Viewer.")

        self.__factory = SofaFactory(root_node=root_node, render_graph=render_graph)
        self.__vedo_thread: Optional[threading.Thread] = None
        self.__animation_player = animation_player

    def launch(self):

        def __launch(socket_port: int):
            subprocess.run([executable, vedo_viewer.__file__, str(socket_port), str(self.__animation_player)])

        port = self.__factory.init()
        self.__vedo_thread = threading.Thread(target=__launch, args=(port,), daemon=True)
        self.__vedo_thread.start()
        self.__factory.connect()

    def render(self):

        self.__factory.update()

    def shutdown(self):

        self.__factory.close()
        self.__vedo_thread.join()
