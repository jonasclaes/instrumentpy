# Copyright 2022 Jonas Claes
# SPDX-License-Identifier: Apache-2.0
"""Specify a serial device, using the common device interface."""
import serial as pyserial
from instrumentpy.common.common_device_interface import CommonDeviceInterface


class SerialDevice(CommonDeviceInterface):
    """
    Serial devices are simple devices, making use of a RS232 connection
    or a serial-over-USB connection using an FTDI or CH343 chip for example.
    """
    _serial: pyserial.Serial = None

    def __init__(self, serial: pyserial.Serial) -> None:
        super().__init__()
        self._serial = serial

    def send_command(self, data: bytes) -> bool:
        """
        Send a command through the serial connection.

        Encoding happens because typically these serial instruments
        don't understand UTF-8 and ask for binary encoded characters.
        """
        if self._serial.is_open is False:
            self._serial.open()

        return self._serial.write(data)

    def receive_output(self, length=1) -> bytes:
        """
        Receive command output through the serial connection.

        Decoding happens because typically these serial instruments
        don't understand UTF-8 and ask for binary encoded characters.
        They also return this, so we have to decode our binary encoded string.
        """
        if self._serial.is_open is False:
            self._serial.open()

        return self._serial.readline()
