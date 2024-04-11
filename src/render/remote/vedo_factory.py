from typing import List
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from vedo import Points, Plotter

from SofaRender.render.remote.vedo_memory import VedoMemory
from SofaRender.render.components import COMPONENTS, BaseComponent
from SofaRender.render.utils import fix_memory_leak


class VedoFactory:

    def __init__(self, port: int, plt: Plotter):

        fix_memory_leak()  # CPython issue: https://github.com/python/cpython/issues/82300

        # Connect to the server process
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server.connect(('localhost', port))

        # Get each object information
        nb_objects = int.from_bytes(self.server.recv(2), 'big')
        self.memories: List[VedoMemory] = []
        self.components: List[BaseComponent] = []

        for _ in range(nb_objects):
            component_type = self.server.recv(int.from_bytes(self.server.recv(2), 'big')).decode('utf-8')
            memory = VedoMemory(server=self.server)
            self.components.append(COMPONENTS[component_type](data=memory))
            self.components[-1].create()

        self.busy = False
        self.plt = plt
        self.step_idx = 0

        self.update_times = []

    def start(self):

        self.server.send(b'done')

        # Launch communication loop
        thread = Thread(target=self.__communicate)
        thread.start()

    def __communicate(self):

        while (cmd := self.server.recv(4)) != b'done':
            if cmd == b'updt':

                # todo : move the memory on the server side to avoid copies on the client side
                self.step_idx += 1

                # Might be necessary to synchronize buffer read/write access
                # self.server.send(b'1')

        while self.plt.background_renderer is not None:
            pass
        self.close()

    def update_models(self, idx: int):

        for component in self.components:
            component.update(idx=idx)

    def get_objects(self) -> List[Points]:

        return [component.vedo_object for component in self.components]

    def close(self):

        # Close shared memories
        for component in self.components:
            component.data.close()

        # Notify server and close connection
        self.server.send(b'done')
        self.server.recv(4)
        self.server.close()
