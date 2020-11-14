from typing import List
from gym_pycr_pwcrack.dao.container_config.node_flags_config import NodeFlagsConfig

class FlagsConfig:

    def __init__(self, flags : List[NodeFlagsConfig]):
        self.flags = flags