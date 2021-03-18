import gym_pycr_ctf.constants.constants as constants

class RenderConfig:

    def __init__(self, num_levels: int = 3, num_nodes_per_level = 4, render_adj_matrix : bool = False):
        self.resources_dir = constants.RENDERING.RESOURCES_DIR
        self.num_levels = num_levels
        self.num_nodes_per_level = num_nodes_per_level
        self.render_adj_matrix = render_adj_matrix
