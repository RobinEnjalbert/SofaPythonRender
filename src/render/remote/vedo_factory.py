from typing import List, Optional
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from multiprocessing import Pool, cpu_count
from vedo import Plotter, Points

from SofaRender.render.remote.vedo_memory import VedoMemory
from SofaRender.render.components import COMPONENTS, BaseComponent
from SofaRender.render.utils import fix_memory_leak


class VedoFactory:

    def __init__(self, port: int):

        fix_memory_leak()  # CPython issue: https://github.com/python/cpython/issues/82300

        # Connect to the server process
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server.connect(('localhost', port))

        # Get each object information
        nb_objects = int.from_bytes(self.server.recv(2), 'big')
        self.memories: List[VedoMemory] = []
        self.components: List[BaseComponent] = []

        from time import time
        start = time()
        for _ in range(nb_objects):
            component_type = self.server.recv(int.from_bytes(self.server.recv(2), 'big')).decode('utf-8')
            memory = VedoMemory(server=self.server)
            self.components.append(COMPONENTS[component_type](data=memory))
            self.components[-1].create()
        # threads = []
        # for component in self.components:
        #     t = Thread(target=component.create)
        #     threads.append(t)
        #     t.start()
        # for t in threads:
        #     t.join()
        print('CREATION TIME = ', time() - start)

        self.server.send(b'done')

        # Launch communication loop
        thread = Thread(target=self.__communicate)
        thread.start()

    def __communicate(self):

        while (cmd := self.server.recv(4)) != b'done':
            if cmd == b'updt':
                self.update()
                # Might be necessary to synchronize buffer read/write access
                # self.server.send(b'done')

        self.close()

    def update(self):
        pass

    def get_objects(self) -> List[Points]:

        return [component.vedo_object for component in self.components]

    def update_objects(self, plt: Plotter, idx: Optional[int] = None) -> None:

        pass

    def close(self):

        # Close shared memories
        for component in self.components:
            component.data.close()

        # Notify server and close connection
        self.server.send(b'done')
        self.server.recv(4)
        self.server.close()
