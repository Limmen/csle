from typing import List
from gym_pycr_pwcrack.dao.container_config.node_users_config import NodeUsersConfig

class UsersConfig:

    def __init__(self, users : List[NodeUsersConfig]):
        self.users = users