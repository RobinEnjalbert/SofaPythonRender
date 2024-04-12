from typing import Dict, Optional, Tuple
import numpy as np
from socket import socket
from multiprocessing.shared_memory import SharedMemory


class VedoMemory:

    def __init__(self, server: socket, store_data: bool):

        # Receive the shared memories for display flag
        sm_name = server.recv(int.from_bytes(server.recv(2), 'big')).decode('utf-8')
        self.__display_flag_buffer = SharedMemory(create=False, name=sm_name)
        self.__display_flag = np.ndarray(shape=(), dtype=bool, buffer=self.__display_flag_buffer.buf)

        # Receive shared memories for data
        self.__data: Dict[str, Tuple[np.ndarray, np.ndarray]] = {}
        self.__data_buffers: Dict[str, Tuple[SharedMemory, SharedMemory]] = {}
        nb_data_fields = int.from_bytes(server.recv(2), 'big')
        for _ in range(nb_data_fields):

            # Shared memory name
            sm_name = server.recv(int.from_bytes(server.recv(2), 'big')).decode('utf-8')
            data_sm = SharedMemory(create=False, name=sm_name)
            dirty_sm = SharedMemory(create=False, name=f'{sm_name}_dirty')
            # Data field name
            field_name = server.recv(int.from_bytes(server.recv(2), 'big')).decode('utf-8')
            # Data shape
            shape = np.frombuffer(server.recv(int.from_bytes(server.recv(2), 'big'))).astype(int).reshape(-1)
            # Data type
            dtype = np.dtype(server.recv(int.from_bytes(server.recv(2), 'big')).decode('utf-8'))

            self.__data_buffers[field_name] = (data_sm, dirty_sm)
            flag = np.array(0, dtype=bool)
            self.__data[field_name] = (np.ndarray(shape=shape, dtype=dtype, buffer=data_sm.buf),
                                       np.ndarray(shape=flag.shape, dtype=flag.dtype, buffer=dirty_sm.buf))

        # Data storage for animation player
        if store_data:
            self.memory = {field_name: [] for field_name in self.__data.keys()}
            self.get_data = self.__get_data_store
        else:
            self.get_data = self.__get_data

    def __get_data(self, field_name: str, link_name: str = 'self') -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:

        return self.__data.get(f'{link_name}.{field_name}', (None, None))

    def __get_data_store(self, field_name: str, link_name: str = 'self') -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:

        data, dirty = self.__data.get(f'{link_name}.{field_name}', (None, None))
        if data is not None:
            self.memory[f'{link_name}.{field_name}'].append(np.array(data))
        return data, dirty

    def get_frame(self, idx: int, field_name: str, link_name: str = 'self') -> Optional[np.ndarray]:

        data = self.memory.get(f'{link_name}.{field_name}', None)
        return None if data is None else data[idx]

    def close(self):

        # Close the display flag shared memory
        self.__display_flag_buffer.close()

        # Close each data shared memory
        for (data_sm, dirty_sm) in self.__data_buffers.values():
            data_sm.close()
            dirty_sm.close()
