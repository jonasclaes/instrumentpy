# Copyright 2022 Jonas Claes
# SPDX-License-Identifier: Apache-2.0
"""Common device interface."""


class CommonDeviceInterface():
    """Common device interface."""

    def send_command(self, data: bytes) -> bool:
        """Send a command over a connection to a device."""

    def receive_output(self, length: int = 1) -> bytes:
        """Receive output over a connection from a device."""
