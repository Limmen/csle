from typing import List, Tuple

class NodeUsersConfig:

    def __init__(self, ip: str, users: List[Tuple[str, str, bool]]):
        self.ip = ip
        self.users = users