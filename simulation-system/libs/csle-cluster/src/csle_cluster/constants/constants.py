"""
Constants for csle-cluster
"""

from typing import Dict, Any


class KIBANA_TUNNELS:
    """
    Constants related to Kibana tunnels
    """
    KIBANA_TUNNELS_DICT: Dict[str, Dict[str, Any]] = {}
    KIBANA_TUNNEL_BASE_PORT = 17000
    THREAD_PROPERTY = "thread"


class RYU_TUNNELS:
    """
    Constants related to Ryu tunnels
    """
    RYU_TUNNELS_DICT: Dict[str, Dict[str, Any]] = {}
    RYU_TUNNEL_BASE_PORT = 18000
    THREAD_PROPERTY = "thread"
