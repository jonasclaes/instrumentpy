# Copyright 2022 Jonas Claes
# SPDX-License-Identifier: Apache-2.0
"""Specify a TCP/IP device, using the common device interface."""
from socket import AF_INET, SOCK_STREAM
import socket
from instrumentpy.common.common_device_interface import CommonDeviceInterface


class TCPIPDevice(CommonDeviceInterface):
    """
    TCP/IP device which connects through a socket.
    """
    _socket: socket.socket = None

    def __init__(self, ip_address, port) -> None:
        super().__init__()
        self._socket = socket.socket(AF_INET, SOCK_STREAM)
        self._socket.connect((ip_address, port))

    def send_command(self, data: bytes) -> bool:
        """
        Send a command through the socket connection.
        """
        return self._socket.send(data)

    def receive_output(self, length=1) -> bytes:
        """
        Receive command output through the socket connection.
        """
        return self._socket.recv(length)
