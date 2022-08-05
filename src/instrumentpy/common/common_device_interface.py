# Copyright 2022 Jonas Claes
# SPDX-License-Identifier: Apache-2.0
"""Common device interface."""


class CommonDeviceInterface():
    """Common device interface."""

    def send_command(self, data: str) -> bool:
        """Send a command over a connection to a device."""

    def receive_output(self, lines: int = 1) -> str:
        """Receive output over a connection from a device."""
