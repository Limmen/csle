from typing import List
from gym_pycr_pwcrack.dao.node_type import NodeType
from gym_pycr_pwcrack.dao.flag import Flag

class Node:

    def __init__(self, ip: str, ip_id: int, id : int, type: NodeType, flags: List[Flag], level : int):
        self.ip = ip
        self.ip_id = ip_id
        self.id = id
        self.type = type
        self.flags = flags
        self.level = level