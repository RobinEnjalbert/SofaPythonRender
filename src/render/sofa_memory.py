from typing import Dict, Tuple
from numpy import ndarray, array
from socket import socket
from multiprocessing.shared_memory import SharedMemory
import Sofa

from SofaRender.render.components import BaseConfig


class SofaMemory:

    def __init__(self,
                 sofa_object: Sofa.Core.Object,
                 config: BaseConfig):

        self.sofa_object = sofa_object
        self.sofa_node: Sofa.Core.Node = self.sofa_object.getLinks()[0].getLinkedBase()

        # Check display flag existence in the Data fields
        if self.sofa_object.getData('display_flag') is None:
            self.sofa_object.addData(name='display_flag', type='bool', value=False)
            
        # Create a shared memory object for display flag
        flag = array(0, dtype=bool)
        self.__display_flag_buffer = SharedMemory(create=True, size=flag.nbytes)
        self.__display_flag = ndarray(shape=flag.shape, dtype=bool, buffer=self.__display_flag_buffer.buf)

        # Create shared memory for object Data
        self.__data_buffers: Dict[str, Tuple[SharedMemory, SharedMemory]] = {}
        self.__data_fields: Dict[str, Sofa.Core.Data] = {}
        self.__data: Dict[str, Tuple[ndarray, ndarray]] = {}
        for field_name in config.object_fields:
            if self.sofa_object.findData(field_name) is None:
                raise ValueError(f'Error in config for {self.sofa_object.getClassName()}: Data field {field_name} '
                                 f'does not exist.')
            self.__create_field_memory(field_name=f'self.{field_name}',
                                       data_field=self.sofa_object.getData(field_name))

        # Create shared memory for linked Data
        for link_name, field_names in config.linked_fields.items():
            if self.sofa_object.findLink(link_name) is not None:
                linked_object = self.sofa_object.findLink(link_name).getLinkedBase()
            elif self.sofa_node.findLink(link_name) is not None:
                linked_object = self.sofa_node.findLink(link_name).getLinkedBase()
            else:
                raise ValueError(f'Error in config for {self.sofa_object.getClassName()}: Link {link_name} not found.')
            for field_name in field_names:
                if linked_object.findData(field_name) is None:
                    raise ValueError(f'Error in config for {self.sofa_object.getClassName()}: Data field {field_name} '
                                     f'does not exist in the linked object {linked_object.getClassName()}.')
                self.__create_field_memory(field_name=f'{link_name}.{field_name}',
                                           data_field=linked_object.getData(field_name))

    def __create_field_memory(self, field_name: str, data_field: Sofa.Core.Data):

        data = data_field.value if isinstance(data_field.value, ndarray) else array(data_field.value)
        dirty = array(0, dtype=bool)
        if data.nbytes > 0:
            data_sm = SharedMemory(create=True, size=data.nbytes)
            dirty_sm = SharedMemory(create=True, size=dirty.nbytes, name=f'{data_sm.name}_dirty')
            self.__data_buffers[field_name] = (data_sm, dirty_sm)
            self.__data[field_name] = (ndarray(shape=data.shape, dtype=data.dtype, buffer=data_sm.buf),
                                       ndarray(shape=dirty.shape, dtype=dirty.dtype, buffer=dirty_sm.buf))
            self.__data[field_name][0][...] = data[...]
            self.__data[field_name][1][...] = dirty[...]
            self.__data_fields[field_name] = data_field

    def connect(self, client: socket):

        # Send the component type
        component_type = self.sofa_object.getClassName().encode('utf-8')
        client.send(len(component_type).to_bytes(2, 'big'))
        client.send(component_type)

        # Send the display flag shared memory
        sm_name = self.__display_flag_buffer.name.encode('utf-8')
        client.send(len(sm_name).to_bytes(2, 'big'))
        client.send(sm_name)

        # Send data shared memories
        client.send(len(self.__data).to_bytes(2, 'big'))
        for field_name, data in self.__data.items():
            # Shared memory name
            sm_name = self.__data_buffers[field_name][0].name.encode('utf-8')
            client.send(len(sm_name).to_bytes(2, 'big'))
            client.send(sm_name)
            # Data field name
            client.send(len(field_name.encode('utf-8')).to_bytes(2, 'big'))
            client.send(field_name.encode('utf-8'))
            # Data shape
            shape = array(data[0].shape, dtype=float)
            client.send(shape.nbytes.to_bytes(2, 'big'))
            client.send(shape.tobytes())
            # Data type
            dtype = data[0].dtype.str.encode('utf-8')
            client.send(len(dtype).to_bytes(2, 'big'))
            client.send(dtype)

    def update(self):

        for field_name in self.__data.keys():
            data = self.__data_fields[field_name].value
            data = data if isinstance(data, ndarray) else array(data)
            if (data[...] == self.__data[field_name][0]).all():
                self.__data[field_name][0][...] = data[...]
                self.__data[field_name][1][...] = True

    def close(self):

        # Close display flag shared memory
        self.__display_flag_buffer.close()
        self.__display_flag_buffer.unlink()

        # Close each data shared memory
        for (data_sm, dirty_sm) in self.__data_buffers.values():
            data_sm.close()
            data_sm.unlink()
            dirty_sm.close()
            dirty_sm.unlink()
