from typing import List, Tuple

class NodeFlagsConfig:

    def __init__(self, ip: str, flags: List[Tuple[str, str, str, id, bool, int]]):
        self.ip = ip
        # flags= [(name, path, id, root, score)]
        self.flags = flags
