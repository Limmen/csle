"""
The main frame for the pycr-ctf environment
"""
import pyperclip
import os
import pyglet
from gym_pycr_ctf.envs.rendering.util.render_util import batch_rect_fill, batch_line, batch_label, \
    create_circle_fill, batch_rect_border
import gym_pycr_ctf.constants.constants as constants
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.agent.attacker_agent_state import AttackerAgentState
from gym_pycr_ctf.dao.observation.attacker_machine_observation_state import AttackerMachineObservationState
from gym_pycr_ctf.envs import PyCRCTFEnv
from gym_pycr_ctf.dao.network.env_mode import EnvMode
class MainFrame(pyglet.window.Window):
    """
    A class representing the OpenGL/Pyglet Game Frame
    By subclassing pyglet.window.Window, event handlers can be defined simply by overriding functions, e.g.
    event handler for on_draw is defined by overriding the on_draw function.
    """

    def __init__(self, env_config: EnvConfig, init_state : AttackerAgentState, env: PyCRCTFEnv = None):
        """
        Initialize frame
        :param env_config: trhe environment config
        :param init_state: the initial state to render
        """

        # call constructor of parent class
        super(MainFrame, self).__init__(height=850, width=1400, caption=constants.RENDERING.CAPTION)
        self.env_config = env_config
        self.env = env
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
        self.firewall_sprites = {}
        self.setup_resources_path()
        self.state = init_state
        self.node_ip_to_coords = {}
        self.node_ip_to_node = {}
        self.node_ip_to_ip_lbl = {}
        self.node_ip_to_links = {}
        self.node_ip_to_idx = {}
        self.node_idx = 0
        self.id_to_node = {}
        self.gui_queue = []
        self.gui_queue_reset = []
        self.complete_graph_links = {}
        self.adj_matrix_labels = []
        self.adj_matrix_columns = []
        self.adj_matrix_rows = []
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
        self.node_idx = 0

        nodes_to_coords = {}
        coords = []

        # Draw hacker
        self.hacker_avatar = pyglet.resource.image(constants.RENDERING.HACKER_SPRITE_NAME)
        self.hacker_sprite = pyglet.sprite.Sprite(self.hacker_avatar, x=self.width/2, y=self.height-35, batch=self.batch,
                                                    group=self.background)
        self.hacker_sprite.scale = 0.18

        lbl = batch_label("." + self.env_config.hacker_ip.rsplit(".", 1)[-1], self.width / 2 + 50,
                    self.height - 20, 10, (0, 0, 0, 255), self.batch, self.second_foreground)
        self.node_ip_to_ip_lbl[self.env_config.hacker_ip] = lbl
        nodes_to_coords[int(self.env_config.hacker_ip.rsplit(".", 1)[-1])] = (self.width/2+20,self.height-35)
        coords.append((self.width/2+20,self.height-35))
        self.node_ip_to_coords[self.env_config.hacker_ip] = (self.width / 2 + 20, self.height - 35)
        hacker_m = AttackerMachineObservationState(ip=self.env_config.hacker_ip)
        self.node_ip_to_node[self.env_config.hacker_ip] = hacker_m
        self.id_to_node[int(self.env_config.hacker_ip.rsplit(".", 1)[-1])] = hacker_m
        self.node_ip_to_idx[self.env_config.hacker_ip] = self.node_idx
        self.node_idx += 1
        self.gui_queue_reset.append((lbl, self.env_config.hacker_ip, (self.width/2+20,self.height-35)))

        # Draw subnet Mask
        batch_label(str(self.env_config.network_conf.subnet_mask), self.width / 2 + 175,
                    self.height - 20, 10, (0, 0, 0, 255), self.batch, self.second_foreground, bold=True)

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

        # Draw manual action label
        batch_label("Manual Action:", self.width / 2 + 350,
                    self.height - 25, 10, (0, 0, 0, 255), self.batch, self.second_foreground, bold=False)
        self.manual_action_label = batch_label(str(self.state.manual_action), self.width / 2 + 450,
                                     self.height - 25, 10, (0, 0, 0, 255), self.batch, self.second_foreground,
                                     bold=False)

        # Draw manual action instructions
        batch_label("Input ID", self.width / 2 + 330,
                    self.height - 50, 10, (0, 0, 0, 255), self.batch, self.second_foreground, bold=False)
        batch_label("[Enter]: execute", self.width / 2 + 350,
                    self.height - 75, 10, (0, 0, 0, 255), self.batch, self.second_foreground, bold=False)
        batch_label("[ESC]: reset", self.width / 2 + 340,
                    self.height - 100, 10, (0, 0, 0, 255), self.batch, self.second_foreground, bold=False)
        batch_label("[TAB]: print actions", self.width / 2 + 360,
                    self.height - 125, 10, (0, 0, 0, 255), self.batch, self.second_foreground, bold=False)

        # Draw router
        y_sep = 40
        create_circle_fill(self.width / 2 + 20, self.height - 60, 3, self.batch, self.first_foreground,
                           constants.RENDERING.WHITE)
        lbl = batch_label("", self.width / 2 + 40,
                    self.height - 60, 10, (0, 0, 0, 255), self.batch, self.second_foreground)
        self.node_ip_to_ip_lbl[self.env_config.router_ip] = lbl
        nodes_to_coords[int(self.env_config.router_ip.rsplit(".", 1)[-1])] = (self.width / 2 + 20, self.height - 60)
        coords.append((self.width / 2 + 20, self.height - 60))
        self.node_ip_to_coords[self.env_config.router_ip] = (self.width / 2 + 20, self.height - 60)
        machine = AttackerMachineObservationState(ip=self.env_config.router_ip)
        self.node_ip_to_node[self.env_config.router_ip] = machine
        self.id_to_node[int(self.env_config.router_ip.rsplit(".", 1)[-1])] = machine
        self.node_ip_to_idx[self.env_config.router_ip] = self.node_idx
        self.node_idx += 1
        self.gui_queue_reset.append((lbl, None, (self.width / 2 + 20, self.height - 60)))

        # --- Draw adjacency matrix
        if self.env_config.render_config.render_adj_matrix:
            adj_matrix_x_start = 150
            adj_matrix_y_start = self.height - 45
            h = 15
            w = 15

            # Draw Adjacency Matrix label
            batch_label("Adjacency Matrix:", adj_matrix_x_start + ((self.env_config.num_nodes+1)*w)/2,
                        self.height - 10, 10, (0, 0, 0, 255), self.batch, self.second_foreground, bold=False)

            self.adj_matrix_labels = []
            self.adj_matrix_columns = []
            self.adj_matrix_rows = []
            y_adj = adj_matrix_y_start
            for m in range(self.env_config.num_nodes+1):
                row = batch_label(".xxx", adj_matrix_x_start -10, y_adj - m*h + w/3, 5,
                                (0, 0, 0, 255), self.batch,
                                self.second_foreground)
                row.font_size = 6
                self.adj_matrix_rows.append(row)
                col = batch_label(".xxx", adj_matrix_x_start + m * w + w/2, y_adj+20, 5,
                                  (0, 0, 0, 255), self.batch,
                                  self.second_foreground)
                col.font_size = 6
                self.adj_matrix_columns.append(col)

            for m in range(self.env_config.num_nodes+1):
                row_labels = []
                #y_adj = y_adj - (m * h) + w / 3
                y_temp = y_adj - (m * h) + w / 3
                for c in range(self.env_config.num_nodes+1):
                    batch_rect_border(adj_matrix_x_start + c * w, adj_matrix_y_start - (m * h), w, h, constants.RENDERING.BLACK, self.batch,
                                      self.background)
                    l = batch_label("0", adj_matrix_x_start + w / 2 + c * (w), y_temp, 8,
                                    (0, 0, 0, 255), self.batch,
                                    self.second_foreground)
                    l.font_size = 6
                    row_labels.append(l)
                self.adj_matrix_labels.append(row_labels)

            adj_matrix_max_x = adj_matrix_x_start + (self.env_config.num_nodes+2) * w
            adj_matrix_min_y = adj_matrix_y_start - (self.env_config.num_nodes + 2) * h
        else:
            adj_matrix_max_x = 150
            adj_matrix_min_y = self.height - 45

        # --- Draw Topology --

        # Draw nodes
        x_max = self.width - 100
        num_nodes_in_level = self.env_config.render_config.num_nodes_per_level
        x_sep = 50
        y_sep = 25
        max_nodes_per_level = int(x_max / x_sep + 1)
        middle = self.width / 2
        x_start = middle - (((num_nodes_in_level - 1) / 2) * x_sep)
        x_start = max(adj_matrix_max_x + 15, x_start)
        x = x_start
        y = self.height-100
        self.flag_avatar = pyglet.resource.image(constants.RENDERING.FLAG_SPRITE_NAME)
        self.firewall_avatar = pyglet.resource.image(constants.RENDERING.FIREWALL_SPRITE_NAME)
        for level in range(self.env_config.render_config.num_levels):
            if level > 1:
                x = x_start
                for n in range(num_nodes_in_level):
                    # if x > x_max:
                    #     x = x_start
                    create_circle_fill(x, y, 3, self.batch, self.first_foreground, constants.RENDERING.WHITE)
                    lbl = batch_label("", x -20, y-6, 10, (0, 0, 0, 255), self.batch,
                                self.second_foreground)
                    lbl.font_size = 10
                    i=0
                    flag_sprite = pyglet.sprite.Sprite(self.flag_avatar, x=x-(15*(i+1)),
                                                            y=y+2,
                                                            batch=self.batch,
                                                            group=self.background)
                    flag_sprite.scale = 0.04
                    flag_sprite.visible = False
                    self.gui_queue.append((lbl, flag_sprite, (x,y)))
                    coords.append((x,y))
                    self.flags_sprites.append((flag_sprite, machine.ip))
                    x = x + x_sep
                y = y - y_sep

        if self.env_config.network_conf.nodes is not None and len(self.env_config.network_conf.nodes) > 0 \
            and self.env_config.network_conf.adj_matrix is not None and len(self.env_config.network_conf.adj_matrix) > 0:
            for n1 in self.env_config.network_conf.nodes:
                machine = self.state.get_machine(n1.ip)
                if machine is not None:
                    for n2 in self.env_config.network_conf.nodes:
                        if self.env_config.network_conf.adj_matrix[n1.id-1][n2.id-1] == 1:
                            machine.reachable.add(n2.ip)
                    if machine.ip == self.env_config.router_ip:
                        machine.reachable.add(self.env_config.hacker_ip)
                        machine.reachable.add(self.env_config.router_ip)
        #
        # Draw links
        for c1 in coords:
            for c2 in coords:
                color = constants.RENDERING.WHITE
                links = []

                # draw first straight line down
                c_1 = c1[0]
                c_2 = c1[1]
                c_3 = c1[0]
                c_4 = c1[1] - (c1[1] - c2[1]) / 2
                l = batch_line(c_1, c_2, c_3, c_4, color, self.batch, self.background, constants.RENDERING.LINE_WIDTH)
                links.append((c_1,c_2,c_3,c_4))
                # draw horizontal line
                c_1 = c1[0]
                c_2 = c1[1] - (c1[1] - c2[1]) / 2
                c_3 = c2[0]
                c_4 = c1[1] - (c1[1] - c2[1]) / 2
                l2 = batch_line(c_1, c_2, c_3, c_4, color, self.batch, self.background,
                               constants.RENDERING.LINE_WIDTH)
                links.append((c_1, c_2, c_3, c_4))
                # draw second straight line down
                c_1 = c2[0]
                c_2 = c1[1] - (c1[1] - c2[1]) / 2
                c_3 = c2[0]
                c_4 = c2[1]
                l3 = batch_line(c_1, c_2, c_3, c_4, color, self.batch, self.background,
                               constants.RENDERING.LINE_WIDTH)
                links.append((c_1, c_2, c_3, c_4))
                self.complete_graph_links[(c1, c2)] = links

        self.gui_queue.reverse()
        self.gui_queue_reset = self.gui_queue.copy() + self.gui_queue_reset

        w = 20
        h = 15
        y = min(min(y + 40, self.height-150), adj_matrix_min_y)
        x_start = 10
        end_state_x = x_start + (self.state.machines_state.shape[1]+2)*w
        # Draw State title
        batch_label("State", end_state_x/2,
                    y, 8, (0, 0, 0, 255), self.batch, self.second_foreground, bold=True)

        y = y-15
        labels = ["m", "ip", "os"]
        for i in range(self.state.attacker_obs_state.num_ports):
            labels.append("p" + str(i))
        for i in range(self.state.attacker_obs_state.num_vuln):
            labels.append("v" + str(i))

        labels.append("#o_p")
        labels.append("#v")
        labels.append("s(cvss)")
        labels.append("sh")
        labels.append("p")
        labels.append("root")
        labels.append("flags")

        for i in range(self.state.attacker_obs_state.num_sh):
            labels.append("sh_" + str(i))

        labels.append("tools")
        labels.append("bd")

        # Draw labels
        for c in range(self.state.machines_state.shape[1]):
            batch_label(labels[c], x_start+w/2+c*(w), y, 5, (0, 0, 0, 255), self.batch,
                        self.second_foreground)
        y = y - 20

        # Draw state
        self.state_labels = []
        state_rect_coords = {}
        for m in range(self.state.machines_state.shape[0]):
            c_labels = []
            for c in range(self.state.machines_state.shape[1]):
                batch_rect_border(x_start+c*w, y-(m*h), w, h, constants.RENDERING.BLACK, self.batch, self.background)
                #y_s = y-(m*h)+w/2
                y_s = y - (m * h) + w / 3
                state_rect_coords[(m,c)] = (x_start+c*w,y-(m*h))
                l = batch_label(str(self.state.machines_state[m][c]), x_start+w/2 + c * (w), y_s, 5, (0, 0, 0, 255), self.batch,
                            self.second_foreground)
                c_labels.append(l)
            self.state_labels.append(c_labels)

        self.state_rect_coords = state_rect_coords

        y_log = y

        # Draw Ports Table

        y = y_s - 45
        w = 20
        h = 15

        batch_label("Ports", 85,
                    y_s - 15, 8, (0, 0, 0, 255), self.batch, self.second_foreground, bold=True)

        labels = ["m", "p", "s_id", "udp/tcp", "service"]
        for c in range(len(labels)):
            if c == 0:
                batch_label(labels[c], int(x_start+10 + c * w), y_s-25, 5, (0, 0, 0, 255), self.batch, self.second_foreground)
            elif c == 2:
                batch_label(labels[c], int(x_start + 10 + (c+1) * w), y_s - 25, 5, (0, 0, 0, 255), self.batch,
                            self.second_foreground)
            elif c == 3:
                batch_label(labels[c], int(x_start + 15 + (c + 1) * w), y_s - 25, 5, (0, 0, 0, 255), self.batch,
                            self.second_foreground)
            elif c == 1:
                batch_label(labels[c], int(x_start +20 + c * w), y_s - 25, 5, (0, 0, 0, 255), self.batch,
                            self.second_foreground)
            else:
                batch_label(labels[c], int(x_start+30 + (c+1) * w), y_s - 25, 5, (0, 0, 0, 255), self.batch,
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
                p_0_l = batch_label(str(self.state.ports_state[p][0]), int(x_start+10 + 0 * w), y_p+w/3, 5, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                p_1_l = batch_label(str(self.state.ports_state[p][1]), int(x_start+10 + 1.5 * w), y_p + w / 3, 5, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                p_2_l = batch_label(str(self.state.ports_state[p][2]), int(x_start+20 + 2.5 * w), y_p + w / 3, 5, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                p_3_l = batch_label(str(self.state.ports_state[p][3]), int(x_start + 20 + 3.5 * w), y_p + w / 3, 5,
                                    (0, 0, 0, 255),
                                    self.batch,
                                    self.second_foreground)
                service = "-" if self.state.ports_state[p][2] not in self.state.service_lookup else str(self.state.service_lookup[self.state.ports_state[p][2]])
                p_4_l = batch_label(service, int(x_start+75 + 2.5 * w), y_p + w / 3, 5, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                p_lbls = [p_0_l, p_1_l, p_2_l, p_3_l, p_4_l]
                self.ports_labels.append(p_lbls)


        # Draw Vulnerabilities Table
        batch_label("Vulnerabilities", 280,
                    y_s - 15, 8, (0, 0, 0, 255), self.batch, self.second_foreground, bold=True)

        labels = ["v", "vulnerability", "cvss"]
        for c in range(len(labels)):
            if c == 0:
                batch_label(labels[c], 210 + 0 * w, y_s - 25, 5, (0, 0, 0, 255), self.batch,
                            self.second_foreground)
            elif c == 1:
                batch_label(labels[c], 250+1*w, y_s - 25, 5, (0, 0, 0, 255), self.batch,
                            self.second_foreground)
            elif c == 2:
                batch_label(labels[c], 310 + 1 * w, y_s - 25, 5, (0, 0, 0, 255), self.batch,
                            self.second_foreground)
        v_n = 0
        self.vuln_labels = []
        for v_name, v_id in self.state.vuln_lookup.items():
            y_v = int(y - (v_n * h))
            if y_v > 5:
                batch_rect_border(200 + 0 * w, y_v, w, h, constants.RENDERING.BLACK, self.batch,
                                  self.background)
                batch_rect_border(200 + 1 * w, y_v, w * 5, h, constants.RENDERING.BLACK, self.batch,
                                  self.background)
                batch_rect_border(200 + 6 * w, y_v, w, h, constants.RENDERING.BLACK, self.batch,
                                  self.background)
                v_lbl_0 = batch_label("-", 210 + 0*w, y_v + w / 2.5,
                            5, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                v_lbl_1 = batch_label("-", 250+ 1 * w, y_v + w / 2.5,
                            5, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                v_lbl_2 = batch_label("-", 290 + 2 * w, y_v + w / 2.5,
                                      5, (0, 0, 0, 255),
                                      self.batch,
                                      self.second_foreground)
                self.vuln_labels.append([v_lbl_0, v_lbl_1, v_lbl_2])
            v_n += 1

        # Draw OS Table

        batch_label("OS", 410,
                    y_s - 15, 8, (0, 0, 0, 255), self.batch, self.second_foreground, bold=True)

        labels = ["os_id", "os"]
        for c in range(len(labels)):
            if c != 1:
                batch_label(labels[c], 370 + 0 * w, y_s - 25, 5, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
            else:
                batch_label(labels[c], 405 + 1 * w, y_s - 25, 5, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)

        o_n = 0
        self.os_labels = []
        for os_name, os_id in self.state.os_lookup.items():
            y_o = int(y - (o_n * h))
            if y_o > 5:
                batch_rect_border(360 + 0 * w, y_o, w, h, constants.RENDERING.BLACK,
                                  self.batch,
                                  self.background)
                batch_rect_border(360 + 1 * w, y_o, w * 5, h, constants.RENDERING.BLACK,
                                  self.batch,
                                  self.background)
                o_lbl_0 = batch_label("-", 370 + 0 * w, y_o + w / 2.5,
                            5, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                o_lbl_1 = batch_label("-", 405 + 1 * w, y_o + w / 2.5,
                            5, (0, 0, 0, 255),
                            self.batch,
                            self.second_foreground)
                self.os_labels.append([o_lbl_0, o_lbl_1])
                end_state_x_log= max(610, end_state_x)
            o_n += 1

        # Draw log
        # Draw Log title
        #log_x = end_state_x_log + (self.width - end_state_x_log) / 2
        log_x = 1000
        #y_log = y_s - 25
        y = min(min(y + 40, self.height - 150), adj_matrix_min_y)
        batch_label("Log", log_x,
                    y_log, 8, (0, 0, 0, 255), self.batch, self.second_foreground, bold=True)
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

    def on_key_press(self, symbol, modifiers) -> None:
        """
        Event handler for on_key_press event.
        The user can move the agent with key presses.
        :param symbol: the symbol of the keypress
        :param modifiers: _
        :return: None
        """
        # Dont do anything if agent is playing
        if not self.env_config.manual_play:
            return

        if symbol == pyglet.window.key._1:
            self.state.manual_action = self.state.manual_action + "1"
        elif symbol == pyglet.window.key._2:
            self.state.manual_action = self.state.manual_action + "2"
        elif symbol == pyglet.window.key._3:
            self.state.manual_action = self.state.manual_action + "3"
        elif symbol == pyglet.window.key._4:
            self.state.manual_action = self.state.manual_action + "4"
        elif symbol == pyglet.window.key._5:
            self.state.manual_action = self.state.manual_action + "5"
        elif symbol == pyglet.window.key._6:
            self.state.manual_action = self.state.manual_action + "6"
        elif symbol == pyglet.window.key._7:
            self.state.manual_action = self.state.manual_action + "7"
        elif symbol == pyglet.window.key._8:
            self.state.manual_action = self.state.manual_action + "8"
        elif symbol == pyglet.window.key._9:
            self.state.manual_action = self.state.manual_action + "9"
        elif symbol == pyglet.window.key._0:
            self.state.manual_action = self.state.manual_action + "0"
        elif symbol == pyglet.window.key.ENTER:
            if self.env is not None:
                # action = int(self.state.manual_action)
                # self.env.step(action)
                #try:
                actions = list(map(lambda x: int(x), self.state.manual_action.split(",")))
                #action = int(self.state.manual_action)
                for a in actions:
                    _, _, done, _ = self.env.step(a)
                    if done:
                        print("done:{}".format(done))
                # except Exception as e:
                #     print("invalid action: {}".format(str(e)))
            self.state.manual_action = ""
        elif symbol == pyglet.window.key.BACKSPACE:
            self.state.manual_action = self.state.manual_action[:-1]
        elif symbol == pyglet.window.key.ESCAPE:
            if self.env is not None:
                self.env.reset()
        elif symbol == pyglet.window.key.TAB:
            if self.env is not None:
                self.env.env_config.attacker_action_conf.print_actions()
        elif modifiers is 18 and pyglet.window.key.MOD_CTRL and int(symbol) is pyglet.window.key.V:
            self.state.manual_action = pyperclip.paste()

        elif modifiers is 18 and pyglet.window.key.MOD_CTRL and int(symbol) is pyglet.window.key.C:
            pyperclip.copy(self.state.manual_action)

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
            match = False
            for machine in self.state.attacker_obs_state.machines:
                if sp_fl[1] == machine.ip and len(machine.flags_found) > 0:
                    match = True
            sp_fl[0].visible = match

    def update_labels(self) -> None:
        """
        Helper function that updates labels with the new state

        :return: None
        """
        self.c_r_label.text = str(round(self.state.cumulative_reward))
        self.n_e_label.text = str(self.state.num_episodes)
        self.r_label.text = str(round(self.state.episode_reward, 1))
        self.t_label.text = str(self.state.time_step)
        self.n_d_label.text = str(self.state.num_detections)
        self.n_af_label.text = str(self.state.num_all_flags)
        self.manual_action_label.text = str(self.state.manual_action)
        for m in range(len(self.state_labels)):
            for c in range(len(self.state_labels[m])):
                self.state_labels[m][c].text = str(int(self.state.machines_state[m][c]))
                if len(str(int(self.state.machines_state[m][c]))) > 3:
                    self.state_labels[m][c].font_size = 4
                else:
                    self.state_labels[m][c].font_size = 6
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
            if i < num_logs:
                self.log_labels[i].text = str(num_logs - 1 - i) + ":" + self.state.env_log.log[num_logs - 1 - i]
            else:
                self.log_labels[i].text = ""

        for v in range(len(self.vuln_labels)):
            if v <= len(self.state.vuln_state)-1:
                self.vuln_labels[v][0].text = str(int(self.state.vuln_state[v][0]))
                vuln_name = "-" if int(self.state.vuln_state[v][0]) not in self.state.vuln_lookup_inv else str(
                    self.state.vuln_lookup_inv[int(self.state.vuln_state[v][0])])
                self.vuln_labels[v][1].text = vuln_name
                self.vuln_labels[v][2].text = str(int(self.state.vuln_state[v][1]))
                if len(str(int(self.state.vuln_state[v][0]))) > 4:
                    self.vuln_labels[v][0].font_size = 4
                else:
                    self.vuln_labels[v][0].font_size = 6

        for o in range(len(self.os_labels)):
            if o < len(self.state.os_state):
                self.os_labels[o][0].text = str(int(self.state.os_state[o][0]))
                os_name = "-" if int(self.state.os_state[o][0]) not in self.state.os_state else str(
                    self.state.os_lookup_inv[int(self.state.os_state[o][0])])
                self.os_labels[o][1].text = os_name
                self.os_labels[o][1].font_size = 6

    def update_topology(self):

        # Reset
        for i in range(len(self.gui_queue_reset)):
            lbl, flag_sprite, (x, y) = self.gui_queue_reset[i]
            if flag_sprite != self.env_config.hacker_ip:
                create_circle_fill(x, y, 3, self.batch, self.first_foreground,
                                   constants.RENDERING.WHITE)
                lbl.text = ""
            for _,links in self.node_ip_to_links.items():
                for link in links:
                    batch_line(link[0], link[1], link[2], link[3], constants.RENDERING.WHITE, self.batch, self.background,
                               constants.RENDERING.LINE_WIDTH)
            for j in range(len(self.gui_queue_reset)):
                _, _, (x2, y2) = self.gui_queue_reset[j]
                links = self.complete_graph_links[(x,y), (x2,y2)]
                for link in links:
                    batch_line(link[0], link[1], link[2], link[3], constants.RENDERING.WHITE, self.batch, self.background,
                                   constants.RENDERING.LINE_WIDTH)

        if self.env_config.render_config.render_adj_matrix:
            for i in range(len(self.adj_matrix_labels)):
                self.adj_matrix_rows[i].text = ".xxx"
                self.adj_matrix_columns[i].text = ".xxx"
                self.adj_matrix_columns[i].font_size = 6
                for lbl in self.adj_matrix_labels[i]:
                    lbl.text = "0"
                    lbl.font_size = 6

        self.node_ip_to_links = {}

        for fw in self.firewall_sprites.values():
            fw.visible = False

        drawn_links = set()
        new_machine_links = False
        for x in self.state.attacker_obs_state.machines:
            if x.ip not in self.node_ip_to_coords:
                self.add_new_node_to_gui(x)
            if x.ip not in self.node_ip_to_links:
                new_machine_links = True

        if new_machine_links:
            self.add_new_links_to_gui()

        for x in self.state.attacker_obs_state.machines:
            machine = self.node_ip_to_node[x.ip]
            if machine.ip == self.env_config.hacker_ip:
                continue
            coords = self.node_ip_to_coords[machine.ip]
            if machine.ip == self.env_config.router_ip:
                color = constants.RENDERING.BLUE_PURPLE
            else:
                color = constants.RENDERING.BLACK
            if x.logged_in:
                color = constants.RENDERING.GREEN
            create_circle_fill(coords[0], coords[1], 3, self.batch, self.first_foreground, color)
            lbl = self.node_ip_to_ip_lbl[machine.ip]
            lbl.text = "." + str(machine.ip.rsplit(".", 1)[-1])
            if machine.ip in self.node_ip_to_links:
                for link in self.node_ip_to_links[machine.ip]:
                    if (link[0], link[1], link[2], link[3]) not in drawn_links and (link[2], link[3], link[0], link[1]) \
                            not in drawn_links:
                        batch_line(link[0], link[1], link[2], link[3], constants.RENDERING.BLACK, self.batch,
                                   self.background,
                                   constants.RENDERING.LINE_WIDTH)
                        drawn_links.add((link[0], link[1], link[2], link[3]))
                        drawn_links.add((link[2], link[3], link[0], link[1]))
            if self.env_config.render_config.render_adj_matrix:
                self.adj_matrix_columns[self.node_ip_to_idx[machine.ip]].text = "." + machine.ip.rsplit(".", 1)[-1]
                self.adj_matrix_rows[self.node_ip_to_idx[machine.ip]].text = "." + machine.ip.rsplit(".", 1)[-1]
                reachable = machine.reachable.copy()
                if machine.ip == self.env_config.router_ip:
                    reachable = machine.reachable.union(self.state.attacker_obs_state.agent_reachable)
                for machine2 in reachable:
                    if machine.ip in self.node_ip_to_idx and machine2 in self.node_ip_to_idx:
                        self.adj_matrix_labels[self.node_ip_to_idx[machine.ip]][self.node_ip_to_idx[machine2]].text = "1"
            # if m.ip in self.firewall_sprites:
            #     fw_sprite = self.firewall_sprites[m.ip]
            #     fw_sprite.visible = True

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

    def set_state(self, state : AttackerAgentState) -> None:
        """
        Sets the render state

        :param state: the new state
        :return: None
        """
        num_nodes = len(state.attacker_obs_state.machines)
        num_nodes_prev = len(self.state.attacker_obs_state.machines)
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

    def update(self, dt) -> None:
        """
        Event handler for the update-event (timer-based typically), used to update the state of the grid.

        :param dt: the number of seconds since the function was last called
        :return: None
        """
        if self.env_config.manual_play and self.env is not None:
            self.set_state(self.env.attacker_agent_state)
        else:
            self.set_state(self.state)
        self.on_draw()

    def reset_state(self):
        self.node_ip_to_links = {}

    def add_new_node_to_gui(self, machine: AttackerMachineObservationState):
        try:
            lbl, flag_sprite, (x, y) = self.gui_queue.pop()
            self.node_ip_to_ip_lbl[machine.ip] = lbl
            self.node_ip_to_coords[machine.ip] = (x, y)
            self.node_ip_to_node[machine.ip] = machine
            if machine.ip not in self.node_ip_to_idx:
                self.node_ip_to_idx[machine.ip] = self.node_idx
                self.node_idx += 1
            self.flags_sprites.append((flag_sprite, machine.ip))
            self.id_to_node[int(machine.ip.rsplit(".", 1)[-1])] = machine
        except IndexError as e:
            print("Too many nodes for GUI, increase GUI size: {}".format(str(e)))

    def add_new_links_to_gui(self):
        self.node_ip_to_links = {}
        if self.env_config.env_mode == EnvMode.SIMULATION or \
            self.env_config.env_mode == EnvMode.GENERATED_SIMULATION:

            if self.env_config.network_conf.nodes is not None and len(self.env_config.network_conf.nodes) > 0 \
                    and self.env_config.network_conf.adj_matrix is not None and len(
                self.env_config.network_conf.adj_matrix) > 0:
                for n1 in self.env_config.network_conf.nodes:
                    machine = self.state.get_machine(n1.ip)
                    if machine is not None:
                        for n2 in self.env_config.network_conf.nodes:
                            if self.env_config.network_conf.adj_matrix[n1.id - 1][n2.id - 1] == 1:
                                machine.reachable.add(n2.ip)
                        if machine.ip == self.env_config.router_ip:
                            machine.reachable.add(self.env_config.hacker_ip)
                            machine.reachable.add(self.env_config.router_ip)

        for machine in self.state.attacker_obs_state.machines:
            machine1_links = []
            #print("self.node_ip_to_coords:{}".format(self.node_ip_to_coords))
            coords1 = self.node_ip_to_coords[machine.ip]
            reachable = machine.reachable.copy()
            if machine.ip == self.env_config.router_ip:
                reachable = machine.reachable.union(self.state.attacker_obs_state.agent_reachable)
            for machine2 in reachable:
                if machine2 not in self.node_ip_to_node:
                    continue
                machine2 = self.node_ip_to_node[machine2]
                coords2 = self.node_ip_to_coords[machine2.ip]

                color = constants.RENDERING.WHITE
                node2_links = []

                links = self.complete_graph_links[(coords1, coords2)]

                if machine.ip == self.env_config.hacker_ip or machine.ip == self.env_config.router_ip:
                    machine1_links.append(links[0])
                node2_links.append(links[0])

                # draw horizontal line
                node2_links.append(links[1])

                # # draw second straight line down
                if machine.ip == self.env_config.hacker_ip or machine.ip == self.env_config.router_ip:
                    machine1_links.append(links[2])
                node2_links.append(links[2])

                if machine2.ip not in self.node_ip_to_links:
                    self.node_ip_to_links[machine2.ip] = node2_links
                else:
                    self.node_ip_to_links[machine2.ip] = self.node_ip_to_links[machine2.ip] + node2_links

            if machine.ip not in self.node_ip_to_links:
                self.node_ip_to_links[machine.ip] = machine1_links
            else:
                self.node_ip_to_links[machine.ip] = self.node_ip_to_links[machine.ip] + machine1_links

