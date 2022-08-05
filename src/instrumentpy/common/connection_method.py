"""Contains the enum for possible connection methods."""
from enum import Enum


class ConnectionMethod(Enum):
    """An enum of possible connection methods for instruments."""
    SERIAL = 1
    TCP_IP = 2
    VISA = 3
