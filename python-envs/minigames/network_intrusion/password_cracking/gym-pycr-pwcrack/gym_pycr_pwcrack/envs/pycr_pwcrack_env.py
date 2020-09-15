from typing import Union
import gym
from abc import ABC
import numpy as np
import os
from gym_pycr_pwcrack.dao.env.env_config import EnvConfig
from gym_pycr_pwcrack.dao.agent.agent_state import AgentState
from gym_pycr_pwcrack.dao.env.env_state import EnvState
from gym_pycr_pwcrack.dao.agent.agent_log import AgentLog
import gym_pycr_pwcrack.constants.constants as constants
from gym_pycr_pwcrack.envs.logic.transition_operator import TransitionOperator
from gym_pycr_pwcrack.dao.env.node import Node
from gym_pycr_pwcrack.dao.env.flag import Flag
from gym_pycr_pwcrack.dao.env.node_type import NodeType
from gym_pycr_pwcrack.dao.env.network_config import NetworkConfig
from gym_pycr_pwcrack.dao.render.render_config import RenderConfig
from gym_pycr_pwcrack.dao.env.env_mode import EnvMode
from gym_pycr_pwcrack.dao.action.action_config import ActionConfig, NMAPActions
from gym_pycr_pwcrack.dao.env.cluster_config import ClusterConfig
from gym_pycr_pwcrack.dao.env.network_service import NetworkService
from gym_pycr_pwcrack.dao.env.transport_protocol import TransportProtocol
from gym_pycr_pwcrack.dao.env.vulnerability import Vulnerability

class PyCRPwCrackEnv(gym.Env, ABC):
    """
    TODO
    """

    def __init__(self, env_config : EnvConfig):
        self.env_config = env_config
        self.env_state = EnvState(network_config=self.env_config.network_conf, num_ports=self.env_config.num_ports,
                                  num_vuln=self.env_config.num_vuln)
        self.agent_state = AgentState(obs_state=self.env_state.obs_state, env_log=AgentLog(),
                                      service_lookup=constants.SERVICES.service_lookup,
                                      vuln_lookup=constants.VULNERABILITIES.vuln_lookup,
                                      os_lookup = constants.OS.os_lookup)
        self.observation_space = gym.spaces.Box(low=0, high=10, dtype=np.int32, shape=(10, 10,))
        self.reward_range = (float(0), float(1))
        self.num_states = 100
        self.viewer = None
        self.steps_beyond_done = None
        self.metadata = {
            'render.modes': ['human', 'rgb_array'],
            'video.frames_per_second': 50  # Video rendering speed
        }
        self.step_outcome = None

    # -------- API ------------
    def step(self, action_id : int) -> Union[np.ndarray, int, bool, dict]:
        """
        Takes a step in the environment by executing the given action

        :param action_id: the action to take
        :return: (obs, reward, done, info)
        """
        info = {}
        if action_id > len(self.env_config.action_conf.actions)-1:
            raise ValueError("Action ID: {} not recognized".format(action_id))
        action = self.env_config.action_conf.actions[action_id]
        s_prime, reward, done = TransitionOperator.transition(s=self.env_state, a=action, env_config=self.env_config)
        self.env_state = s_prime
        obs = self.env_state.get_observation()
        self.agent_state.time_step += 1
        self.agent_state.episode_reward += reward
        self.agent_state.obs_state = self.env_state.obs_state
        sn_tag = "sn" if action.subnet else "h"
        self.agent_state.env_log.add_entry(action.name + "[" + sn_tag + "]")
        return obs, reward, done, info

    def reset(self) -> np.ndarray:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :return: initial observation
        """
        self.env_state.reset_state()
        obs = self.env_state.get_observation()
        self.agent_state.num_episodes += 1
        self.agent_state.cumulative_reward += self.agent_state.episode_reward
        self.agent_state.time_step = 0
        self.agent_state.episode_reward = 0
        return obs

    def render(self, mode: str = 'human'):
        """
        Renders the environment
        Supported rendering modes:
        - human: render to the current display or terminal and
          return nothing. Usually for human consumption.
        - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
          representing RGB values for an x-by-y pixel image, suitable
          for turning into a video.
        :param mode: the rendering mode
        :return: True (if human mode) otherwise an rgb array
        """
        if mode not in self.metadata["render.modes"]:
            raise NotImplemented("mode: {} is not supported".format(mode))
        if self.viewer is None:
            self.__setup_viewer()
        self.viewer.mainframe.set_state(self.agent_state)
        arr = self.viewer.render(return_rgb_array=mode == 'rgb_array')
        return arr

    def close(self) -> None:
        """
        Closes the viewer (cleanup)
        :return: None
        """
        if self.viewer:
            self.viewer.close()
            self.viewer.mainframe.new_window()
            self.viewer = None

    # -------- Private methods ------------
    def __setup_viewer(self):
        """
        Setup for the viewer to use for rendering
        :return: None
        """
        from gym_pycr_pwcrack.envs.rendering.viewer import Viewer
        script_dir = os.path.dirname(__file__)
        resource_path = os.path.join(script_dir, './rendering/frames/', constants.RENDERING.RESOURCES_DIR)
        self.env_config.render_config.resources_dir = resource_path
        self.viewer = Viewer(env_config=self.env_config, init_state=self.agent_state)
        self.viewer.start()

# -------- Concrete envs ------------

# -------- Difficulty 1 (Simple) ------------

# -------- Version 1 ------------
class PyCRPwCrackSimpleSim1Env(PyCRPwCrackEnv):

    def __init__(self, env_config: EnvConfig):
        if env_config is None:
            nodes = [Node(ip="172.18.1.10", ip_id=10, id=1, type=NodeType.ROUTER, flags=[], level=2, services=[],
                          os="linux", vulnerabilities=[]),
                     Node(ip="172.18.1.2", ip_id=2, id=2, type=NodeType.SERVER,
                          flags=[Flag(name="flag2", path="/home/kim", id=2)], level=3, os="linux",
                          services=[
                              NetworkService(protocol=TransportProtocol.TCP, port=22, name="ssh"),
                              NetworkService(protocol=TransportProtocol.TCP, port=53, name="domain"),
                              NetworkService(protocol=TransportProtocol.TCP, port=80, name="http"),
                              NetworkService(protocol=TransportProtocol.TCP, port=9042, name="cassandra"),
                              NetworkService(protocol=TransportProtocol.TCP, port=9160, name="cassandra"),
                              NetworkService(protocol=TransportProtocol.UDP, port=53, name="domain"),
                          ],
                          vulnerabilities=[
                              Vulnerability(name="ssh-weak-password", cve=None, cvss=10.0, exploits=[],
                                            port=22, protocol=TransportProtocol.TCP),
                              Vulnerability(name="CVE-2014-9278", cve="CVE-2014-9278", cvss=4.0, exploits=[],
                                            port=22, protocol=TransportProtocol.TCP),
                              Vulnerability(name="CVE-2020-8620", cve="CVE-2020-8620", cvss=5.0, exploits=[],
                                            port=53, protocol=TransportProtocol.TCP),
                              Vulnerability(name="CVE-2020-8617", cve="CVE-2020-8617", cvss=5.0,exploits=[],
                                            port=53, protocol=TransportProtocol.TCP),
                              Vulnerability(name="CVE-2020-8616", cve="CVE-2020-8616", cvss=5.0,exploits=[],
                                            port=53, protocol=TransportProtocol.TCP),
                              Vulnerability(name="CVE-2019-6470", cve="CVE-2019-6470", cvss=5.0,exploits=[],
                                            port=53, protocol=TransportProtocol.TCP),
                              Vulnerability(name="CVE-2020-8623", cve="CVE-2020-8623", cvss=4.3,exploits=[],
                                            port=53, protocol=TransportProtocol.TCP),
                              Vulnerability(name="CVE-2020-8621", cve="CVE-2020-8621", cvss=4.3,exploits=[],
                                            port=53, protocol=TransportProtocol.TCP),
                              Vulnerability(name="CVE-2020-8624", cve="CVE-2020-8624", cvss=4.0,exploits=[],
                                            port=53, protocol=TransportProtocol.TCP),
                              Vulnerability(name="CVE-2020-8622", cve="CVE-2020-8622", cvss=4.0,exploits=[],
                                            port=53, protocol=TransportProtocol.TCP),
                              Vulnerability(name="CVE-2020-8619", cve="CVE-2020-8619", cvss=4.0,exploits=[],
                                            port=53, protocol=TransportProtocol.TCP),
                              Vulnerability(name="CVE-2020-8618", cve="CVE-2020-8618", cvss=4.0,exploits=[],
                                            port=53, protocol=TransportProtocol.TCP)
                          ]
                          ),
                     Node(ip="172.18.1.3", ip_id=3, id=3, type=NodeType.SERVER, os="linux",
                          flags=[Flag(name="flag1", path="/home/admin", id=1)], level=3,
                          services=[
                              NetworkService(protocol=TransportProtocol.TCP, port=23,name="telnet"),
                              NetworkService(protocol=TransportProtocol.TCP, port=80, name="http")
                          ], vulnerabilities=[
                             Vulnerability(name="CVE-2020-15523", cve="CVE-2020-15523", cvss=6.9, exploits=[], port=80,
                                           protocol=TransportProtocol.TCP),
                             Vulnerability(name="CVE-2020-14422", cve="CVE-2020-14422", cvss=4.3, exploits=[], port=80,
                                           protocol=TransportProtocol.TCP),
                             Vulnerability(name="telnet-weak-password", cve=None, cvss=10.0, exploits=[],
                                           port=23, protocol=TransportProtocol.TCP)
                         ]
                          ),
                     Node(ip="172.18.1.21", ip_id=21, id=4, type=NodeType.SERVER, flags=[], level=3, os="linux",
                          services=[
                              NetworkService(protocol=TransportProtocol.TCP, port=25, name="smtp"),
                              NetworkService(protocol=TransportProtocol.TCP, port=2181, name="kafka"),
                              NetworkService(protocol=TransportProtocol.TCP, port=5432, name="postgresql"),
                              NetworkService(protocol=TransportProtocol.TCP, port=6667, name="irc"),
                              NetworkService(protocol=TransportProtocol.TCP, port=9092, name="kafka"),
                              NetworkService(protocol=TransportProtocol.TCP, port=38969, name="kafka"),
                              NetworkService(protocol=TransportProtocol.TCP, port=42843, name="kafka"),
                              NetworkService(protocol=TransportProtocol.UDP, port=123, name="ntp"),
                              NetworkService(protocol=TransportProtocol.UDP, port=161, name="snmp")
                          ],
                          vulnerabilities=[]),
                     Node(ip="172.18.1.79", ip_id=79, id=5, type=NodeType.SERVER,
                          flags=[Flag(name="flag3", path="/home/euler", id=3),
                                 Flag(name="flag4", path="/home/euler", id=4)], level=3,
                          os="linux",
                          services=[
                              NetworkService(protocol=TransportProtocol.TCP, port=21, name="ftp"),
                              NetworkService(protocol=TransportProtocol.TCP, port=79, name="finger"),
                              NetworkService(protocol=TransportProtocol.TCP, port=8009, name="ajp13"),
                              NetworkService(protocol=TransportProtocol.TCP, port=8080, name="http"),
                              NetworkService(protocol=TransportProtocol.TCP, port=10011, name="teamspeak"),
                              NetworkService(protocol=TransportProtocol.TCP, port=10022, name="teamspeak"),
                              NetworkService(protocol=TransportProtocol.TCP, port=30033, name="teamspeak"),
                              NetworkService(protocol=TransportProtocol.TCP, port=27017, name="mongod"),
                          ],
                          vulnerabilities=[]
                          ),
                     Node(ip="172.18.1.191", ip_id=191, id=6, type=NodeType.HACKER, flags=[], level=1, services=[],
                          os="linux", vulnerabilities=[
                             Vulnerability(name="CVE-2014-9278", cve="CVE-2014-9278", cvss=4.0, exploits=[], port=22,
                                           protocol=TransportProtocol.TCP),
                             Vulnerability(name="ftp-weak-password", cve=None, cvss=10.0, exploits=[],
                                           port=21, protocol=TransportProtocol.TCP)
                         ])]
            subnet_mask = "172.18.1.0/24"
            adj_matrix = [
                [0, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0],
            ]
            network_conf = NetworkConfig(subnet_mask=subnet_mask, nodes=nodes, adj_matrix=adj_matrix)
            render_config = RenderConfig()
            cluster_config = ClusterConfig()
            action_config = ActionConfig(actions=[
                NMAPActions.TCP_SYN_STEALTH_SCAN(ip=network_conf.subnet_mask, subnet=True),
                NMAPActions.PING_SCAN(ip=network_conf.subnet_mask, subnet=True),
                NMAPActions.UDP_PORT_SCAN(ip=network_conf.subnet_mask, subnet=True),
                NMAPActions.TCP_CON_NON_STEALTH_SCAN(ip=network_conf.subnet_mask, subnet=True),
                NMAPActions.TCP_FIN_SCAN(ip=network_conf.subnet_mask, subnet=True),
                NMAPActions.TCP_NULL_SCAN(ip=network_conf.subnet_mask, subnet=True),
                NMAPActions.TCP_XMAS_TREE_SCAN(ip=network_conf.subnet_mask, subnet=True),
                NMAPActions.OS_DETECTION_SCAN(ip=network_conf.subnet_mask, subnet=True),
                NMAPActions.NMAP_VULNERS(ip=network_conf.subnet_mask, subnet=True),
                NMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(ip=network_conf.subnet_mask, subnet=True),
                NMAPActions.SSH_SAME_USER_PASS_DICTIONARY(ip=network_conf.subnet_mask, subnet=True),
                NMAPActions.FTP_SAME_USER_PASS_DICTIONARY(ip=network_conf.subnet_mask, subnet=True),
                NMAPActions.CASSANDRA_SAME_USER_PASS_DICTIONARY(ip=network_conf.subnet_mask, subnet=True),
                NMAPActions.IRC_SAME_USER_PASS_DICTIONARY(ip=network_conf.subnet_mask, subnet=True),
                NMAPActions.MONGO_SAME_USER_PASS_DICTIONARY(ip=network_conf.subnet_mask, subnet=True),
                NMAPActions.MYSQL_SAME_USER_PASS_DICTIONARY(ip=network_conf.subnet_mask, subnet=True),
                NMAPActions.SMTP_SAME_USER_PASS_DICTIONARY(ip=network_conf.subnet_mask, subnet=True),
                NMAPActions.POSTGRES_SAME_USER_PASS_DICTIONARY(ip=network_conf.subnet_mask, subnet=True),
            ])
            env_config = EnvConfig(network_conf=network_conf, action_conf=action_config, num_ports=10, num_vuln=5,
                                   render_config=render_config, env_mode=EnvMode.SIMULATION, cluster_config=cluster_config)
        super().__init__(env_config=env_config)

# -------- Difficulty 2 (Medium) ------------

# -------- Difficulty 3 (Hard) ------------
