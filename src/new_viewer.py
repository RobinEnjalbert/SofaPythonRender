from typing import Optional
import Sofa
import threading
import subprocess
from sys import executable

from SofaRender.render.sofa_factory import SofaFactory
from SofaRender.render.remote import vedo_viewer


class NewViewer:

    def __init__(self,
                 root_node: Sofa.Core.Node = None,
                 render_graph: bool = True):
        """
        Vedo-based viewer for SOFA scenes.

        :param root_node: Root node of the SOFA scene graph.
        :param render_graph: If True, the scene graph will be explored to automatically create Vedo objects.
        """

        if not root_node.isInitialized():
            raise RuntimeError("You must call 'Sofa.Simulation.init(root_node)' before creating the Viewer.")

        self.factory = SofaFactory(root_node=root_node, render_graph=render_graph)
        self.vedo_thread: Optional[threading.Thread] = None
        pass

    def launch(self):

        def __launch(socket_port: int):
            subprocess.run([executable, vedo_viewer.__file__, str(socket_port)])

        port = self.factory.init()
        self.vedo_thread = threading.Thread(target=__launch, args=(port,), daemon=True)
        self.vedo_thread.start()
        self.factory.connect()

    def render(self):

        self.factory.update()

    def shutdown(self):

        self.factory.close()
        self.vedo_thread.join()

