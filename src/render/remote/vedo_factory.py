from typing import List
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from vedo import Points, Plotter
from numpy import ndarray, array
from multiprocessing.shared_memory import SharedMemory

from SofaRender.render.remote.vedo_memory import VedoMemory
from SofaRender.render.components import COMPONENTS, BaseComponent
from SofaRender.render.utils import fix_memory_leak


class VedoFactory:

    def __init__(self, port: int, plt: Plotter, store_data: bool):

        fix_memory_leak()  # CPython issue: https://github.com/python/cpython/issues/82300

        # Connect to the server process
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server.connect(('localhost', port))

        # Get each object information
        nb_objects = int.from_bytes(self.server.recv(2), 'big')
        self.components: List[BaseComponent] = []

        for _ in range(nb_objects):
            component_type = self.server.recv(int.from_bytes(self.server.recv(2), 'big')).decode('utf-8')
            memory = VedoMemory(server=self.server, store_data=store_data)
            self.components.append(COMPONENTS[component_type](data=memory))
            self.components[-1].create()

        self.sync = self.sync_animation if store_data else lambda: None

        self.busy = False
        self.plt = plt
        self.step_idx = 0

        self.update_times = []

        self.root_sm = SharedMemory(create=False, name='psm_root_node', size=8)
        self.root_time = ndarray(shape=(1,), dtype=float, buffer=self.root_sm.buf)

    def start(self):

        self.server.send(b'done')

        # Launch communication loop
        thread = Thread(target=self.__communicate)
        thread.start()

    def __communicate(self):

        while (cmd := self.server.recv(4)) != b'done':
            if cmd == b'updt':
                self.step_idx += 1
                self.sync()

        while self.plt.background_renderer is not None:
            pass
        self.close()

    def update(self):

        for component in self.components:
            component.update()

    def set_frame(self, idx: int):

        for component in self.components:
            component.set_frame(idx=idx)

    def get_objects(self) -> List[Points]:

        return [component.vedo_object for component in self.components]

    def sync_animation(self):

        if self.plt.is_blocked:
            self.server.send(b'0')
            while self.plt.is_blocked:
                pass
            self.server.send(b'1')
        else:
            self.server.send(b'1')

    def close(self):

        # Close shared memories
        for component in self.components:
            component.data.close()

        # Notify server and close connection
        self.server.send(b'done')
        self.server.recv(4)
        self.server.close()
