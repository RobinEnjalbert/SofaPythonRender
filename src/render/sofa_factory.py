from typing import List, Optional
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
import Sofa
import time

from SofaRender.graph import SofaGraph
from SofaRender.render.sofa_memory import SofaMemory
from SofaRender.render.components import CONFIGS


class SofaFactory:

    def __init__(self,
                 root_node: Sofa.Core.Node,
                 render_graph: bool):

        # fix_memory_leak()

        self.scene_graph = SofaGraph(root_node=root_node)
        self.object_memories: List[SofaMemory] = []
        self.__render_graph = render_graph
        self.__display_flags = {'visual_models': True,
                                'collision_model': False,
                                'behavior_model': False,
                                'force_field': False}
        self.__socket = socket(AF_INET, SOCK_STREAM)
        self.__socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.__client: Optional[socket] = None

    def init(self) -> int:

        # Create the memories for all sofa objects
        for key, sofa_object in self.scene_graph.graph.items():

            # Key format = root.child1.child2.@.Component<name>
            component_type = key.split('@.')[1].split('<')[0]

            # Define the visual style
            if component_type == 'VisualStyle':
                display_flags = sofa_object.displayFlags.value.split('  ')
                for display_flag in display_flags:
                    for model in self.__display_flags.keys():
                        if model.split('_')[0] in display_flag[4:].lower():
                            self.__display_flags[model] = display_flag[:4] == 'show'
                            break

            # Record data
            elif component_type in CONFIGS:
                self.object_memories.append(SofaMemory(sofa_object=sofa_object, config=CONFIGS[component_type]))

        # Get an available port
        self.__socket.bind(('localhost', 0))
        return self.__socket.getsockname()[1]

    def connect(self):

        # Connect to the other process
        self.__socket.listen()
        self.__client, _ = self.__socket.accept()

        # Send each object information to create remote shared memory
        self.__client.send(len(self.object_memories).to_bytes(2, 'big'))
        for object_memory in self.object_memories:
            object_memory.connect(client=self.__client)
        self.__client.recv(4)

    def update(self):

        # Update buffers
        # Todo
        # import time
        # start = time.time()
        for object_memory in self.object_memories:
            object_memory.update()
        # threads = []
        # for object_memory in self.object_memories:
        #     t = Thread(target=object_memory.update)
        #     threads.append(t)
        #     t.start()
        # for t in threads:
        #     t.join()
        # print('Update', time.time() - start)

        # Launch reading access for the client
        self.__client.send(b'updt')
        # Might be necessary to synchronize buffer read/write access
        self.__client.recv(4)
        # time.sleep(0.002)

    def close(self):

        self.__client.send(b'done')
        self.__client.recv(4)
        for memory in self.object_memories:
            memory.close()
        self.__client.send(b'done')
        self.__socket.close()





