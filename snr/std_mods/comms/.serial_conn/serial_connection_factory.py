# from snr.core import *

# from . import serial_connection


# class SerialConnectionFactory(EndpointFactory):
#     def __init__(self, transmit_data_name: str,
#                  query_data_name: str,
#                  firmware_path: str
#                  ) -> None:
#         super().__init__(serial_connection)
#         self.transmit_data_name = transmit_data_name
#         self.query_data_name = query_data_name
#         # TODO: Support updating Arduino firmware on startup
#         self.firmware_path = firmware_path

#     def get(self, parent: NodeProtocol) -> AbstractEndpoint:
#         return serial_connection.SerialConnection(self,
#                                                   parent,
#                                                   "Serial Connection",
#                                                   self.transmit_data_name)
