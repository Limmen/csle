"""
Transport protocols in CSLE
"""
from enum import IntEnum


class TransportProtocol(IntEnum):
    """
    Enum representing the different transport protocols in the network.
    """
    TCP = 0
    UDP = 1

    @staticmethod
    def _from_str(protocol_str: str) -> "TransportProtocol":
        """
        Creates the object from a string
        :param protocol_str: the string to create the object from
        :return: the created object
        """
        if protocol_str is None:
            return None
        if protocol_str.lower() == "tcp":
            return TransportProtocol.TCP
        elif protocol_str.lower() == "udp":
            return TransportProtocol.UDP
        else:
            raise ValueError("Protocol string:{} not recognized".format(protocol_str))
