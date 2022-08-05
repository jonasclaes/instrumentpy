#!/usr/bin/env python3
# Copyright 2022 Jonas Claes
# SPDX-License-Identifier: Apache-2.0

import serial as pyserial
from instrumentpy.common.serial_device import SerialDevice
from instrumentpy.psu.aimtti.mx100tp import MX100TP

serial = pyserial.Serial()
serial.port = '/dev/ttyUSB0'
serial_psu = SerialDevice(serial=serial)
psu = MX100TP(device=serial_psu)
