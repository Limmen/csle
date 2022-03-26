import csle_common.constants.constants as constants


class RenderConfig:
    """
    DTO representing rendering configuration
    """

    def __init__(self, num_levels: int = 3, num_nodes_per_level = 4, render_adj_matrix : bool = False):
        """
        Initializes the DTO

        :param num_levels: the number of visual levels for rendering
        :param num_nodes_per_level: the number of nodes per level
        :param render_adj_matrix: whether to render the adjacency matrix or not
        """
        self.resources_dir = constants.RENDERING.RESOURCES_DIR
        self.num_levels = num_levels
        self.num_nodes_per_level = num_nodes_per_level
        self.render_adj_matrix = render_adj_matrix
