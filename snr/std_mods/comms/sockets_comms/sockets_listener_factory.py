import socket
from typing import List, Optional

from snr.core import *
from snr.protocol import *
from snr.std_mods.comms.sockets_base import sockets_wrapper
from snr.type_defs import *

from . import sockets_listener_loop


class SocketsListenerFactory(LoopFactory):
    def __init__(self,
                 port: int,
                 data_keys: List[DataKey] = [],
                 loop_name: str = "sockets_listener_loop",
                 ) -> None:
        super().__init__([
            sockets_listener_loop,
            sockets_wrapper,
        ])
        self.port = port
        self.data_keys = data_keys
        self.loop_name = loop_name
        self.existing_socket: Optional[socket.socket] = None

    def get(self, parent: NodeProtocol) -> ThreadLoop:
        return sockets_listener_loop.SocketsListenerLoop(self,
                                                         parent,
                                                         self.loop_name,
                                                         self.port,
                                                         self.data_keys,
                                                         self.existing_socket)
