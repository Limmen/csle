import gym_pycr_pwcrack.constants.constants as constants

class RenderConfig:

    def __init__(self, num_levels: int = 3, num_nodes_per_level = 4):
        self.resources_dir = constants.RENDERING.RESOURCES_DIR
        self.num_levels = num_levels
        self.num_nodes_per_level = num_nodes_per_level
