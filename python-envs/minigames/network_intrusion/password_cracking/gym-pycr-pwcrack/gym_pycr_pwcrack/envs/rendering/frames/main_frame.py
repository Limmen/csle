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
        self.flags_sprites = []
        self.setup_resources_path()
        self.state = init_state
        self.create_batch()
        self.set_state(self.state)
        self.switch_to()
        self.state_rect_coords = {}

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

        # Draw C_Reward label
        batch_label("C_R:", 25,
                    self.height - 25, 10, (0, 0, 0, 255), self.batch, self.second_foreground, bold=False)
        self.c_r_label = batch_label(str(self.state.cumulative_reward), 100,
                    self.height - 25, 10, (0, 0, 0, 255), self.batch, self.second_foreground, bold=False)
        # Draw N_E label
        batch_label("N_E:", 25,
                    self.height - 50, 10, (0, 0, 0, 255), self.batch, self.second_foreground, bold=False)
        self.c_r_label = batch_label(str(self.state.num_episodes), 100,
                                     self.height - 50, 10, (0, 0, 0, 255), self.batch, self.second_foreground,
                                     bold=False)
        # Draw R label
        batch_label("R:", 25,
                    self.height - 75, 10, (0, 0, 0, 255), self.batch, self.second_foreground, bold=False)
        self.c_r_label = batch_label(str(self.state.episode_reward), 100,
                                     self.height - 75, 10, (0, 0, 0, 255), self.batch, self.second_foreground,
                                     bold=False)

        # Draw t label
        batch_label("t:", 25,
                    self.height - 100, 10, (0, 0, 0, 255), self.batch, self.second_foreground, bold=False)
        self.c_r_label = batch_label(str(self.state.time_step), 100,
                                     self.height - 100, 10, (0, 0, 0, 255), self.batch, self.second_foreground,
                                     bold=False)

        # Draw router
        if self.env_config.network_conf.router is not None:
            create_circle_fill(self.width / 2 + 20, self.height - 75, 8, self.batch, self.first_foreground,
                               constants.RENDERING.BLUE_PURPLE)
            batch_label("." + str(self.env_config.network_conf.router.ip_id), self.width / 2 + 50,
                        self.height - 75, 12, (0, 0, 0, 255), self.batch, self.second_foreground)
            nodes_to_coords[self.env_config.network_conf.router.id] = (self.width / 2 + 20, self.height - 75)
        else:
            raise ValueError("Router is not defined in network config")

        # --- Draw Topology --

        # Draw nodes
        x_start = 25
        x = x_start
        y = self.height-150
        x_sep = 100
        y_sep = 75
        x_max = self.width-100
        max_nodes_per_level = int(x_max/x_sep+1)
        middle = self.width / 2
        self.flag_avatar = pyglet.resource.image(constants.RENDERING.FLAG_SPRITE_NAME)
        for level in range(len(self.env_config.network_conf.levels_d)):
            if level > 1:
                num_nodes_in_level = len(self.env_config.network_conf.levels_d[level+1])
                x_start = middle-(((num_nodes_in_level-1)/2)*x_sep)
                x = x_start
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
                            for i, flag in enumerate(node.flags):
                                # Draw flag
                                flag_sprite = pyglet.sprite.Sprite(self.flag_avatar, x=x-(20*(i+1)),
                                                                        y=y+10,
                                                                        batch=self.batch,
                                                                        group=self.background)
                                flag_sprite.scale = 0.05
                                self.flags_sprites.append(flag_sprite)

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

        w = 30
        h = 25
        y = y + 40
        x_start = 10
        end_state_x = x_start + (self.state.machines_state.shape[1]+2)*w
        # Draw State title
        batch_label("State", end_state_x/2,
                    y, 12, (0, 0, 0, 255), self.batch, self.second_foreground, bold=True)

        y = y-25
        labels = ["m", "ip", "os"]
        for i in range(self.state.num_ports):
            labels.append("p" + str(i))
        for i in range(self.state.num_vuln):
            labels.append("v" + str(i))
        # Draw labels
        for c in range(self.state.machines_state.shape[1]):
            batch_label(labels[c], x_start+w/2+c*(w), y, 10, (0, 0, 0, 255), self.batch,
                        self.second_foreground)
        y = y - 40
        # Draw state
        state_rect_coords = {}
        for m in range(self.state.machines_state.shape[0]):
            for c in range(self.state.machines_state.shape[1]):
                batch_rect_border(x_start+c*w, y-(m*h), w, h, constants.RENDERING.BLACK, self.batch, self.background)
                y_s = y-(m*h)+w/2
                state_rect_coords[(m,c)] = (x_start+c*w,y-(m*h))
                batch_label(str(self.state.machines_state[m][c]), x_start+w/2 + c * (w), y_s, 10, (0, 0, 0, 255), self.batch,
                            self.second_foreground)

        self.state_rect_coords = state_rect_coords

        y_log = y

        # Draw Ports Table

        y = y_s - 100
        w = 30
        h = 25

        batch_label("Ports", 1.5 * (end_state_x / 6),
                    y_s - 40, 12, (0, 0, 0, 255), self.batch, self.second_foreground, bold=True)

        labels = ["m", "p", "s_id", "service"]
        for c in range(len(labels)):
            if c != 3:
                batch_label(labels[c], int(x_start+15 + c * w), y_s-65, 10, (0, 0, 0, 255), self.batch, self.second_foreground)
            else:
                batch_label(labels[c], int(x_start+30 + c * w), y_s - 65, 10, (0, 0, 0, 255), self.batch,
                            self.second_foreground)

        for p in range(self.state.ports_state.shape[0]):
            y_p = int(y - (p * h))
            if y_p > 5:
                batch_rect_border(int(x_start + 0 * w), y_p, w, h, constants.RENDERING.BLACK, self.batch, self.background)
                batch_rect_border(int(x_start + 1 * w), y_p, w, h, constants.RENDERING.BLACK, self.batch, self.background)
                batch_rect_border(int(x_start + 2 * w), y_p, w, h, constants.RENDERING.BLACK, self.batch, self.background)
                batch_rect_border(int(x_start + 3 * w), y_p, w*3, h, constants.RENDERING.BLACK, self.batch, self.background)
                batch_label(str(self.state.ports_state[p][0]), int(x_start+15 + 0 * w), y_p+w/3, 10, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                batch_label(str(self.state.ports_state[p][1]), int(x_start+15 + 1 * w), y_p + w / 3, 10, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                batch_label(str(self.state.ports_state[p][2]), int(x_start+15 + 2 * w), y_p + w / 3, 10, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                service = "-" if self.state.ports_state[p][2] not in self.state.service_lookup else str(self.state.service_lookup[self.state.ports_state[p][2]])
                batch_label(service, int(x_start+45 + 3 * w), y_p + w / 3, 10, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)


        # Draw Vulnerabilities Table

        batch_label("Vulnerabilities", 4*(end_state_x/6),
                    y_s - 40, 12, (0, 0, 0, 255), self.batch, self.second_foreground, bold=True)

        labels = ["v", "vulnerability"]
        for c in range(len(labels)):
            if c != 1:
                batch_label(labels[c], int(20 + 2.8*(end_state_x/6) + 0 * w), y_s - 65, 10, (0, 0, 0, 255), self.batch,
                            self.second_foreground)
            else:
                batch_label(labels[c], int(80 + 2.8*(end_state_x/6) + 0 * w), y_s - 65, 10, (0, 0, 0, 255), self.batch,
                            self.second_foreground)
        v_n = 0
        for v_name, v_id in self.state.vuln_lookup.items():
            y_v = int(y - (v_n * h))
            if y_v > 5:
                batch_rect_border(int(2.8*(end_state_x/6) + 0 * w), y_v, w, h, constants.RENDERING.BLACK, self.batch,
                                  self.background)
                batch_rect_border(int(2.8*(end_state_x/6) + 1 * w), y_v, w * 5, h, constants.RENDERING.BLACK, self.batch,
                                  self.background)
                batch_label(str(v_id), int(15 + 2.8*(end_state_x/6) + 0 * w), y_v + w / 2.5,
                            10, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                batch_label(str(v_name), int(60 + 2.8 * (end_state_x / 6) + 1 * w), y_v + w / 2.5,
                            10, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
            v_n += 1

        # Draw OS Table

        batch_label("OS", 6.5 * (end_state_x / 6),
                    y_s - 40, 12, (0, 0, 0, 255), self.batch, self.second_foreground, bold=True)

        labels = ["os_id", "os"]
        for c in range(len(labels)):
            if c != 1:
                batch_label(labels[c], int(20 + 5.5 * (end_state_x / 6) + 0 * w), y_s - 65, 10, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
            else:
                batch_label(labels[c], int(80 + 5.5 * (end_state_x / 6) + 0 * w), y_s - 65, 10, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)

        o_n = 0
        for os_name, os_id in self.state.os_lookup.items():
            y_o = int(y - (o_n * h))
            if y_o > 5:
                batch_rect_border(int(5.5 * (end_state_x / 6) + 0 * w), y_o, w, h, constants.RENDERING.BLACK,
                                  self.batch,
                                  self.background)
                batch_rect_border(int(5.5 * (end_state_x / 6) + 1 * w), y_o, w * 5, h, constants.RENDERING.BLACK,
                                  self.batch,
                                  self.background)
                batch_label(str(os_id), int(15 + 5.5 * (end_state_x / 6) + 0 * w), y_o + w / 2.5,
                            10, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                batch_label(str(os_name), int(60 + 5.5 * (end_state_x / 6) + 1 * w), y_o + w / 2.5,
                            10, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                end_state_x_log=int(5.5 * (end_state_x / 6) + 1 * w) + w*5
            o_n += 1

        # Draw log

        # Draw Log title
        log_x = end_state_x_log + (self.width - end_state_x_log) / 2
        batch_label("Log", log_x,
                    y_log+60, 12, (0, 0, 0, 255), self.batch, self.second_foreground, bold=True)
        x = log_x
        h = 20
        num_logs = len(self.state.env_log.log)
        for i in range(num_logs):
            y_t = 10 + y_log - ((i - 1) * h)
            if y_t > 25:
                batch_label(self.state.env_log.log[num_logs - 1 - i], x, y_t, 10, (0, 0, 0, 255), self.batch,
                            self.second_foreground)

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

    def set_state(self, state : EnvState):
        self.state = state