"""
The main frame for the pycr-pwcrack environment
"""
import numpy as np
import os
import pyglet
from gym_pycr_pwcrack.envs.rendering.util.render_util import batch_rect_fill, batch_line, batch_label, \
    create_circle_fill, batch_rect_border
import gym_pycr_pwcrack.constants.constants as constants
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.agent.agent_state import AgentState
from gym_pycr_pwcrack.dao.network.node_type import NodeType

class MainFrame(pyglet.window.Window):
    """
    A class representing the OpenGL/Pyglet Game Frame
    By subclassing pyglet.window.Window, event handlers can be defined simply by overriding functions, e.g.
    event handler for on_draw is defined by overriding the on_draw function.
    """

    def __init__(self, env_config: EnvConfig, init_state : AgentState):
        """
        Initialize frame
        :param env_config: trhe environment config
        :param init_state: the initial state to render
        """

        # call constructor of parent class
        super(MainFrame, self).__init__(height=700, width=1300, caption=constants.RENDERING.CAPTION)
        self.env_config = env_config
        self.init_state = init_state
        self.batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.first_foreground = pyglet.graphics.OrderedGroup(1)
        self.second_foreground = pyglet.graphics.OrderedGroup(2)
        self.state_labels = []
        self.ports_labels = []
        self.log_labels = []
        self.vuln_labels = []
        self.os_labels = []
        self.flags_sprites = []
        self.setup_resources_path()
        self.state = init_state
        self.node_ip_to_coords = {}
        self.node_ip_to_node = {}
        self.node_ip_to_ip_lbl = {}
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

        lbl = batch_label("." + str(self.env_config.network_conf.hacker.ip_id), self.width / 2 + 60,
                    self.height - 25, 12, (0, 0, 0, 255), self.batch, self.second_foreground)
        self.node_ip_to_ip_lbl[self.env_config.network_conf.hacker.ip] = lbl
        nodes_to_coords[self.env_config.network_conf.hacker.id] = (self.width/2+20,self.height-50)
        self.node_ip_to_coords[self.env_config.network_conf.hacker.ip] = (self.width / 2 + 20, self.height - 50)
        self.node_ip_to_node[self.env_config.network_conf.hacker.ip] = self.env_config.network_conf.hacker

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
        self.n_e_label = batch_label(str(self.state.num_episodes), 100,
                                     self.height - 50, 10, (0, 0, 0, 255), self.batch, self.second_foreground,
                                     bold=False)
        # Draw R label
        batch_label("R:", 25,
                    self.height - 75, 10, (0, 0, 0, 255), self.batch, self.second_foreground, bold=False)
        self.r_label = batch_label(str(self.state.episode_reward), 100,
                                     self.height - 75, 10, (0, 0, 0, 255), self.batch, self.second_foreground,
                                     bold=False)

        # Draw t label
        batch_label("t:", 25,
                    self.height - 100, 10, (0, 0, 0, 255), self.batch, self.second_foreground, bold=False)
        self.t_label = batch_label(str(self.state.time_step), 100,
                                     self.height - 100, 10, (0, 0, 0, 255), self.batch, self.second_foreground,
                                     bold=False)

        # Draw N_D label
        batch_label("N_D:", 25,
                    self.height - 125, 10, (0, 0, 0, 255), self.batch, self.second_foreground, bold=False)
        self.n_d_label = batch_label(str(self.state.num_detections), 100,
                                   self.height - 125, 10, (0, 0, 0, 255), self.batch, self.second_foreground,
                                   bold=False)

        # Draw N_AF label
        batch_label("N_AF:", 25,
                    self.height - 150, 10, (0, 0, 0, 255), self.batch, self.second_foreground, bold=False)
        self.n_af_label = batch_label(str(self.state.num_all_flags), 100,
                                     self.height - 150, 10, (0, 0, 0, 255), self.batch, self.second_foreground,
                                     bold=False)

        # Draw router
        if self.env_config.network_conf.router is not None:
            create_circle_fill(self.width / 2 + 20, self.height - 75, 8, self.batch, self.first_foreground,
                               constants.RENDERING.WHITE)
            lbl = batch_label("", self.width / 2 + 50,
                        self.height - 75, 12, (0, 0, 0, 255), self.batch, self.second_foreground)
            self.node_ip_to_ip_lbl[self.env_config.network_conf.router.ip] = lbl
            nodes_to_coords[self.env_config.network_conf.router.id] = (self.width / 2 + 20, self.height - 75)
            self.node_ip_to_coords[self.env_config.network_conf.router.ip] = (self.width / 2 + 20, self.height - 75)
            self.node_ip_to_node[self.env_config.network_conf.router.ip] = self.env_config.network_conf.router
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
                            create_circle_fill(x, y, 8, self.batch, self.first_foreground, constants.RENDERING.WHITE)
                            lbl = batch_label("", x - 30, y, 12, (0, 0, 0, 255), self.batch,
                                        self.second_foreground)
                            self.node_ip_to_ip_lbl[node.ip] = lbl
                            for i, flag in enumerate(node.flags):
                                # Draw flag
                                flag_sprite = pyglet.sprite.Sprite(self.flag_avatar, x=x-(20*(i+1)),
                                                                        y=y+10,
                                                                        batch=self.batch,
                                                                        group=self.background)
                                flag_sprite.scale = 0.05
                                flag_sprite.visible = False
                                self.flags_sprites.append((flag_sprite, flag))

                            nodes_to_coords[node.id] = (x, y)
                            self.node_ip_to_coords[node.ip] = (x, y)
                            self.node_ip_to_node[node.ip] = node
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
        for i in range(self.state.obs_state.num_ports):
            labels.append("p" + str(i))
        for i in range(self.state.obs_state.num_vuln):
            labels.append("v" + str(i))

        labels.append("#o_p")
        labels.append("#v")
        labels.append("s(cvss)")
        labels.append("sh")
        labels.append("p")
        labels.append("root")
        labels.append("flags")

        for i in range(self.state.obs_state.num_sh):
            labels.append("sh_" + str(i))

        # Draw labels
        for c in range(self.state.machines_state.shape[1]):
            batch_label(labels[c], x_start+w/2+c*(w), y, 10, (0, 0, 0, 255), self.batch,
                        self.second_foreground)
        y = y - 40

        # Draw state
        self.state_labels = []
        state_rect_coords = {}
        for m in range(self.state.machines_state.shape[0]):
            c_labels = []
            for c in range(self.state.machines_state.shape[1]):
                batch_rect_border(x_start+c*w, y-(m*h), w, h, constants.RENDERING.BLACK, self.batch, self.background)
                y_s = y-(m*h)+w/2
                state_rect_coords[(m,c)] = (x_start+c*w,y-(m*h))
                l = batch_label(str(self.state.machines_state[m][c]), x_start+w/2 + c * (w), y_s, 10, (0, 0, 0, 255), self.batch,
                            self.second_foreground)
                c_labels.append(l)
            self.state_labels.append(c_labels)

        self.state_rect_coords = state_rect_coords

        y_log = y

        # Draw Ports Table

        y = y_s - 100
        w = 30
        h = 25

        batch_label("Ports", 115,
                    y_s - 40, 12, (0, 0, 0, 255), self.batch, self.second_foreground, bold=True)

        labels = ["m", "p", "s_id", "udp/tcp", "service"]
        for c in range(len(labels)):
            if c == 0:
                batch_label(labels[c], int(x_start+15 + c * w), y_s-65, 10, (0, 0, 0, 255), self.batch, self.second_foreground)
            elif c == 2:
                batch_label(labels[c], int(x_start + 10 + (c+1) * w), y_s - 65, 10, (0, 0, 0, 255), self.batch,
                            self.second_foreground)
            elif c == 3:
                batch_label(labels[c], int(x_start + 25 + (c + 1) * w), y_s - 65, 10, (0, 0, 0, 255), self.batch,
                            self.second_foreground)
            elif c == 1:
                batch_label(labels[c], int(x_start +30 + c * w), y_s - 65, 10, (0, 0, 0, 255), self.batch,
                            self.second_foreground)
            else:
                batch_label(labels[c], int(x_start+45 + (c+1) * w), y_s - 65, 10, (0, 0, 0, 255), self.batch,
                            self.second_foreground)
        self.ports_labels = []
        for p in range(self.state.ports_state.shape[0]):
            y_p = int(y - (p * h))
            if y_p > 5:
                batch_rect_border(int(x_start + 0 * w), y_p, w, h, constants.RENDERING.BLACK, self.batch, self.background)
                batch_rect_border(int(x_start + 1 * w), y_p, w*2, h, constants.RENDERING.BLACK, self.batch, self.background)
                batch_rect_border(int(x_start + 3 * w), y_p, w, h, constants.RENDERING.BLACK, self.batch, self.background)
                batch_rect_border(int(x_start + 4 * w), y_p, w, h, constants.RENDERING.BLACK, self.batch, self.background)
                batch_rect_border(int(x_start + 5 * w), y_p, w*3, h, constants.RENDERING.BLACK, self.batch, self.background)
                p_0_l = batch_label(str(self.state.ports_state[p][0]), int(x_start+15 + 0 * w), y_p+w/3, 10, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                p_1_l = batch_label(str(self.state.ports_state[p][1]), int(x_start+15 + 1.5 * w), y_p + w / 3, 10, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                p_2_l = batch_label(str(self.state.ports_state[p][2]), int(x_start+15 + 3 * w), y_p + w / 3, 10, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                p_3_l = batch_label(str(self.state.ports_state[p][3]), int(x_start + 15 + 4 * w), y_p + w / 3, 10,
                                    (0, 0, 0, 255),
                                    self.batch,
                                    self.second_foreground)
                service = "-" if self.state.ports_state[p][2] not in self.state.service_lookup else str(self.state.service_lookup[self.state.ports_state[p][2]])
                p_4_l = batch_label(service, int(x_start+75 + 4 * w), y_p + w / 3, 10, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
            p_lbls = [p_0_l, p_1_l, p_2_l, p_3_l, p_4_l]
            self.ports_labels.append(p_lbls)


        # Draw Vulnerabilities Table

        batch_label("Vulnerabilities", 350,
                    y_s - 40, 12, (0, 0, 0, 255), self.batch, self.second_foreground, bold=True)

        labels = ["v", "vulnerability", "cvss"]
        for c in range(len(labels)):
            if c == 0:
                batch_label(labels[c], 275 + 0 * w, y_s - 65, 10, (0, 0, 0, 255), self.batch,
                            self.second_foreground)
            elif c == 1:
                batch_label(labels[c], 330+1*w, y_s - 65, 10, (0, 0, 0, 255), self.batch,
                            self.second_foreground)
            elif c == 2:
                batch_label(labels[c], 420 + 1 * w, y_s - 65, 10, (0, 0, 0, 255), self.batch,
                            self.second_foreground)
        v_n = 0
        self.vuln_labels = []
        for v_name, v_id in self.state.vuln_lookup.items():
            y_v = int(y - (v_n * h))
            if y_v > 5:
                batch_rect_border(260 + 0 * w, y_v, w, h, constants.RENDERING.BLACK, self.batch,
                                  self.background)
                batch_rect_border(260 + 1 * w, y_v, w * 5, h, constants.RENDERING.BLACK, self.batch,
                                  self.background)
                batch_rect_border(260 + 6 * w, y_v, w, h, constants.RENDERING.BLACK, self.batch,
                                  self.background)
                v_lbl_0 = batch_label("-", 275 + 0*w, y_v + w / 2.5,
                            10, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                v_lbl_1 = batch_label("-", 330+ 1 * w, y_v + w / 2.5,
                            10, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                v_lbl_2 = batch_label("-", 395 + 2 * w, y_v + w / 2.5,
                                      10, (0, 0, 0, 255),
                                      self.batch,
                                      self.second_foreground)
                self.vuln_labels.append([v_lbl_0, v_lbl_1, v_lbl_2])
            v_n += 1

        # Draw OS Table

        batch_label("OS", 580,
                    y_s - 40, 12, (0, 0, 0, 255), self.batch, self.second_foreground, bold=True)

        labels = ["os_id", "os"]
        for c in range(len(labels)):
            if c != 1:
                batch_label(labels[c], 495 + 0 * w, y_s - 65, 10, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
            else:
                batch_label(labels[c], 555 + 1 * w, y_s - 65, 10, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)

        o_n = 0
        self.os_labels = []
        for os_name, os_id in self.state.os_lookup.items():
            y_o = int(y - (o_n * h))
            if y_o > 5:
                batch_rect_border(480 + 0 * w, y_o, w, h, constants.RENDERING.BLACK,
                                  self.batch,
                                  self.background)
                batch_rect_border(480 + 1 * w, y_o, w * 5, h, constants.RENDERING.BLACK,
                                  self.batch,
                                  self.background)
                o_lbl_0 = batch_label("-", 495 + 0 * w, y_o + w / 2.5,
                            10, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                o_lbl_1 = batch_label("-", 555 + 1 * w, y_o + w / 2.5,
                            10, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                self.os_labels.append([o_lbl_0, o_lbl_1])
                end_state_x_log= max(610, end_state_x)
            o_n += 1

        # Draw log

        # Draw Log title
        #log_x = end_state_x_log + (self.width - end_state_x_log) / 2
        log_x = 1000
        y_log = y_s - 40
        batch_label("Log", log_x,
                    y_log, 12, (0, 0, 0, 255), self.batch, self.second_foreground, bold=True)
        y_log = y_log-60
        x = log_x
        h = 20
        max_logs = 100
        num_logs = len(self.state.env_log.log)
        self.log_labels = []
        for i in range(max_logs):
            y_t = 5 + y_log - ((i - 1) * h)
            if y_t > 0:
                l = batch_label("", x, y_t, 10, (0, 0, 0, 255), self.batch,
                            self.second_foreground)
                self.log_labels.append(l)

    def setup_resources_path(self) -> None:
        """
        Setup path to resources (e.g. images)
        :return: None
        """
        script_dir = os.path.dirname(__file__)
        resource_path = os.path.join(script_dir, self.env_config.render_config.resources_dir)
        if os.path.exists(resource_path):
            pyglet.resource.path = [resource_path]
        else:
            raise ValueError("error")
        pyglet.resource.reindex()

    def update_flags(self):
        for sp_fl in self.flags_sprites:
            if sp_fl[1] in self.state.flags_state:
                sp_fl[0].visible = True
            else:
                sp_fl[0].visible = False

    def update_labels(self) -> None:
        """
        Helper function that updates labels with the new state

        :return: None
        """
        self.c_r_label.text = str(self.state.cumulative_reward)
        self.n_e_label.text = str(self.state.num_episodes)
        self.r_label.text = str(self.state.episode_reward)
        self.t_label.text = str(self.state.time_step)
        self.n_d_label.text = str(self.state.num_detections)
        self.n_af_label.text = str(self.state.num_all_flags)
        for m in range(len(self.state_labels)):
            for c in range(len(self.state_labels[m])):
                self.state_labels[m][c].text = str(int(self.state.machines_state[m][c]))
                if len(str(int(self.state.machines_state[m][c]))) > 3:
                    self.state_labels[m][c].font_size = 6
                else:
                    if self.state_labels[m][c].font_size == 6:
                        self.state_labels[m][c].font_size = 10
        for p in range(len(self.ports_labels)):
            for c in range(len(self.ports_labels[p])):
                if c < 4:
                    self.ports_labels[p][c].text = str(int(self.state.ports_state[p][c]))
                else:
                    service = "-" if int(self.state.ports_state[p][2]) not in self.state.service_lookup_inv else str(
                        self.state.service_lookup_inv[int(self.state.ports_state[p][2])])
                    self.ports_labels[p][c].text = service
        num_logs = len(self.state.env_log.log)
        for i in range(len(self.log_labels)):
            if i < num_logs-1:
                self.log_labels[i].text = str(num_logs - 1 - i) + ":" + self.state.env_log.log[num_logs - 1 - i]
            else:
                self.log_labels[i].text = ""

        for v in range(len(self.vuln_labels)):
            self.vuln_labels[v][0].text = str(int(self.state.vuln_state[v][0]))
            vuln_name = "-" if int(self.state.vuln_state[v][0]) not in self.state.vuln_lookup_inv else str(
                self.state.vuln_lookup_inv[int(self.state.vuln_state[v][0])])
            self.vuln_labels[v][1].text = vuln_name
            self.vuln_labels[v][2].text = str(int(self.state.vuln_state[v][1]))
            if len(str(int(self.state.vuln_state[v][0]))) > 3:
                self.vuln_labels[v][0].font_size = 6

        for o in range(len(self.os_labels)):
            if o < len(self.state.os_state):
                self.os_labels[o][0].text = str(int(self.state.os_state[o][0]))
                os_name = "-" if int(self.state.os_state[o][0]) not in self.state.os_state else str(
                    self.state.os_lookup_inv[int(self.state.os_state[o][0])])
                self.os_labels[o][1].text = os_name

    def update_topology(self):
        for node in self.env_config.network_conf.nodes:
            if node.type != NodeType.HACKER:
                coords = self.node_ip_to_coords[node.ip]
                create_circle_fill(coords[0], coords[1], 8, self.batch, self.first_foreground,
                                   constants.RENDERING.WHITE)
        for m in self.state.obs_state.machines:
            node = self.node_ip_to_node[m.ip]
            if node.type == NodeType.HACKER:
                continue
            coords = self.node_ip_to_coords[node.ip]
            if node.type == NodeType.ROUTER:
                color = constants.RENDERING.BLUE_PURPLE
            elif node.type == NodeType.SERVER:
                color = constants.RENDERING.BLACK
            create_circle_fill(coords[0], coords[1], 8, self.batch, self.first_foreground, color)
            lbl = self.node_ip_to_ip_lbl[node.ip]
            lbl.text = "." + str(node.ip_id)


    def on_draw(self) -> None:
        """
        Called every time the frame is updated

        :return: None
        """
        # Clear the window
        self.clear()
        # Draw batch with the frame contents
        self.batch.draw()
        # Update labels
        self.update_labels()
        # Update flags
        self.update_flags()
        # Update topology
        self.update_topology()
        # Make this window the current OpenGL rendering context
        self.switch_to()

    def set_state(self, state : AgentState) -> None:
        """
        Sets the render state

        :param state: the new state
        :return: None
        """
        self.state = state
        self.state.initialize_render_state()

    def new_window(self) -> None:
        """
        Helper function to reset state when creating a new window

        :return: None
        """
        self.batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.first_foreground = pyglet.graphics.OrderedGroup(1)
        self.second_foreground = pyglet.graphics.OrderedGroup(2)