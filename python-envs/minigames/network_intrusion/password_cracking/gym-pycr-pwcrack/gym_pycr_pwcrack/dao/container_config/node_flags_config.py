from typing import List, Tuple

class NodeFlagsConfig:

    def __init__(self, ip: str, flags: List[Tuple[str, str]]):
        self.ip = ip
        self.flags = flags