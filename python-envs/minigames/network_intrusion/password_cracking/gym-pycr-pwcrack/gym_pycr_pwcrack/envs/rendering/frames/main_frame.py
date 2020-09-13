"""
The main frame for the pycr-pwcrack environment
"""
from typing import List
import os
import pyglet
from gym_pycr_pwcrack.envs.rendering.util.render_util import batch_rect_fill, batch_line, batch_label, \
    draw_and_fill_rect, create_circle_fill, create_circle, batch_rect_border
import gym_pycr_pwcrack.constants.constants as constants
from gym_pycr_pwcrack.dao.env_config import EnvConfig
from gym_pycr_pwcrack.dao.env_state import EnvState
from gym_pycr_pwcrack.dao.node_type import NodeType

class MainFrame(pyglet.window.Window):
    """
    A class representing the OpenGL/Pyglet Game Frame
    By subclassing pyglet.window.Window, event handlers can be defined simply by overriding functions, e.g.
    event handler for on_draw is defined by overriding the on_draw function.
    """

    def __init__(self, env_config: EnvConfig, init_state : EnvState):
        # call constructor of parent class
        super(MainFrame, self).__init__(height=700, width=900, caption=constants.RENDERING.CAPTION)
        self.env_config = env_config
        self.init_state = init_state
        self.batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.first_foreground = pyglet.graphics.OrderedGroup(1)
        self.second_foreground = pyglet.graphics.OrderedGroup(2)
        self.setup_resources_path()
        self.state = init_state
        self.create_batch()
        self.set_state(self.state)
        self.switch_to()
        self.y_network_end = 0

    def create_batch(self) -> None:
        """
        Creates a batch of elements to render. By grouping elements in a batch we can utilize OpenGL batch rendering
        and reduce the cpu <–> gpu data transfers and the number of draw-calls.
        :return: None
        """

        # Sets the background color
        batch_rect_fill(0, 0, self.width, self.height, (255, 255, 255), self.batch, self.background)

        nodes_to_coords = {}

        # Draw hacker
        self.hacker_avatar = pyglet.resource.image(constants.RENDERING.HACKER_SPRITE_NAME)
        self.hacker_sprite = pyglet.sprite.Sprite(self.hacker_avatar, x=self.width/2, y=self.height-50, batch=self.batch,
                                                    group=self.background)
        self.hacker_sprite.scale = 0.25
        batch_label("." + str(self.env_config.network_conf.hacker.ip_id), self.width / 2 + 60,
                    self.height - 25, 12, (0, 0, 0, 255), self.batch, self.second_foreground)
        nodes_to_coords[self.env_config.network_conf.hacker.id] = (self.width/2+20,self.height-50)

        # Draw subnet Mask
        batch_label(str(self.env_config.network_conf.subnet_mask), self.width / 2 + 175,
                    self.height - 25, 12, (0, 0, 0, 255), self.batch, self.second_foreground, bold=True)

        # Draw router
        if self.env_config.network_conf.router is not None:
            create_circle_fill(self.width / 2 + 20, self.height - 100, 8, self.batch, self.first_foreground,
                               constants.RENDERING.BLUE_PURPLE)
            batch_label("." + str(self.env_config.network_conf.router.ip_id), self.width / 2 + 50,
                        self.height - 100, 12, (0, 0, 0, 255), self.batch, self.second_foreground)
            nodes_to_coords[self.env_config.network_conf.router.id] = (self.width / 2 + 20, self.height - 100)
        else:
            raise ValueError("Router is not defined in network config")

        # --- Draw Topology --

        # Draw nodes
        x_start = 100
        x = x_start
        y = self.height-200
        x_sep = 100
        y_sep = 100
        x_max = self.width-100
        max_nodes_per_level = int(x_max/x_sep+1)
        for level in range(len(self.env_config.network_conf.levels_d)):
            if level > 1:
                if len(self.env_config.network_conf.levels_d[level+1]) > max_nodes_per_level:
                    raise ValueError("Invalid network config. Too many nodes in a single level. "
                                     "Max level for this width of the GUI is: {}".format(max_nodes_per_level))
                else:
                    for node in self.env_config.network_conf.levels_d[level+1]:
                        if node.type == NodeType.SERVER:
                            if x > x_max:
                                x = x_start
                            create_circle_fill(x, y, 8, self.batch, self.first_foreground, constants.RENDERING.BLACK)
                            batch_label("." + str(node.ip_id), x - 30, y, 12, (0, 0, 0, 255), self.batch,
                                        self.second_foreground)
                            nodes_to_coords[node.id] = (x, y)
                            x = x + x_sep
                y = y - y_sep

        # Draw links
        for i in range(len(self.env_config.network_conf.adj_matrix)):
            for j in range(i+1, len(self.env_config.network_conf.adj_matrix[i])):
                if self.env_config.network_conf.adj_matrix[i][j] == 1:
                    color = constants.RENDERING.BLACK

                    # draw first straight line down
                    batch_line(nodes_to_coords[i + 1][0], nodes_to_coords[i + 1][1],
                                   nodes_to_coords[i + 1][0],  nodes_to_coords[i + 1][1] - (nodes_to_coords[i + 1][1] - nodes_to_coords[j + 1][1])/2,
                                   color, self.batch, self.background, constants.RENDERING.LINE_WIDTH)

                    # draw horizontal line
                    batch_line(nodes_to_coords[i + 1][0], nodes_to_coords[i + 1][1] - (nodes_to_coords[i + 1][1] - nodes_to_coords[j + 1][1]) / 2,
                               nodes_to_coords[j + 1][0],
                               nodes_to_coords[i + 1][1] - (nodes_to_coords[i + 1][1] - nodes_to_coords[j + 1][1]) / 2,
                               color, self.batch, self.background, constants.RENDERING.LINE_WIDTH)

                    # draw second straight line down
                    batch_line(nodes_to_coords[j + 1][0],
                               nodes_to_coords[i + 1][1] - (nodes_to_coords[i + 1][1] - nodes_to_coords[j + 1][1]) / 2,
                               nodes_to_coords[j + 1][0], nodes_to_coords[j+1][1],
                                color, self.batch, self.background, constants.RENDERING.LINE_WIDTH)

        #y = y - 20

        # Draw State title
        batch_label("State", ((self.width / 4)*3)/2,
                    y, 12, (0, 0, 0, 255), self.batch, self.second_foreground, bold=True)
        # Draw Log title
        batch_label("Log", ((self.width / 4) * 3) +  (self.width / 4)/ 2,
                    y, 12, (0, 0, 0, 255), self.batch, self.second_foreground, bold=True)

        y = y-50
        batch_rect_border(50, y, 25, 25, constants.RENDERING.BLACK, self.batch, self.background)

    def setup_resources_path(self) -> None:
        """
        Setup path to resources (e.g. images)
        :return: None
        """
        script_dir = os.path.dirname(__file__)
        resource_path = os.path.join(script_dir, './resources/')
        if os.path.exists(resource_path):
            pyglet.resource.path = [resource_path]
        else:
            raise ValueError("error")
        pyglet.resource.reindex()

    def on_draw(self):
        # Clear the window
        self.clear()
        # Draw batch with the frame contents
        self.batch.draw()
        # Make this window the current OpenGL rendering context
        self.switch_to()

    def set_state(self, state : List):
        self.state = state