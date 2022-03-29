from typing import Tuple
import pickle
from abc import ABCMeta
import numpy as np
import os
import csle_common.constants.constants as constants
from csle_common.dao.envs.base_env import BaseEnv
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.action.attacker.attacker_action import AttackerAction
from gym_csle_stopping_game.util.env_util import EnvUtil


class StoppingGameEnv(BaseEnv, metaclass=ABCMeta):
    """
    Abstract OpenAI Gym Env for the csle-stopping-game
    """

    def __init__(self, emulation_env_config : EmulationEnvConfig):
        self.emulation_env_config = emulation_env_config

        # Initialize environment state
        self.env_state = EmulationEnvState(emulation_env_config=self.emulation_env_config,
                                           service_lookup=constants.SERVICES.service_lookup,
                                           vuln_lookup=constants.VULNERABILITIES.vuln_lookup,
                                           os_lookup=constants.OS.os_lookup)

        # Setup Attacker Spaces
        self.attacker_observation_space = self.env_state.attacker_observation_space
        self.attacker_action_space = self.emulation_env_config.attacker_action_conf.action_space
        self.attacker_num_actions = self.emulation_env_config.attacker_action_conf.num_actions

        # Setup Defender Spaces
        self.defender_observation_space = self.env_state.defender_observation_space
        self.defender_action_space = self.emulation_env_config.defender_action_conf.action_space
        self.defender_num_actions = self.emulation_env_config.defender_action_conf.num_actions

        # Setup Config
        self.viewer = None
        self.metadata = {
            'render.modes': ['human', 'rgb_array'],
            'video.frames_per_second': 50  # Video rendering speed
        }

        # Setup trajectories
        self.trajectories = []

        # Environment state
        self.step = 1
        self.intrusion_state = 0


        # Reset
        self.reset()
        super().__init__()

    # -------- API ------------
    def step(self, action_id : Tuple[int, int]) -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[int, int], bool, dict]:
        """
        Takes a step in the environment by executing the given action

        :param action_id: the action to take
        :return: (obs, reward, done, info)
        """
        if isinstance(action_id, int) or isinstance(action_id, np.int64):
            action_id = (action_id, None)
            print("[WARNING]: This is a multi-agent environment where the input should be "
                  "(attacker_action, defender_action)")

        # TODO
        return None, (0,0), False


    def reset(self, soft : bool = False) -> Tuple[np.ndarray, np.ndarray]:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :return: initial observation
        """
        self.reset_metrics()
        if self.viewer is not None and self.viewer.mainframe is not None:
            self.viewer.mainframe.reset()
        return attacker_m_obs, defender_obs

    def reset_metrics(self) -> None:
        """
        Reset state metrics

        :return: None
        """
        self.step = 1
        self.intrusion_state = 0
        self.__checkpoint_log()
        self.__checkpoint_trajectories()
        self.reset_state()


    def render(self, mode: str = 'human'):
        """
        Renders the environment
        Supported rendering modes:
          -human: render to the current display or terminal and return nothing. Usually for human consumption.
          -rgb_array: Return an numpy.ndarray with shape (x, y, 3),
                      representing RGB values for an x-by-y pixel image, suitable
                      for turning into a video.
        :param mode: the rendering mode
        :return: True (if human mode) otherwise an rgb array
        """
        #self.agent_state.attacker_obs_state = self.env_state.attacker_obs_state.copy()
        if mode not in self.metadata["render.modes"]:
            raise NotImplemented("mode: {} is not supported".format(mode))
        if self.viewer is None:
            self.__setup_viewer()
        self.viewer.mainframe.set_state(None)
        arr = self.viewer.render(return_rgb_array=mode == 'rgb_array')
        return arr

    @staticmethod
    def is_defense_action_legal(defense_action_id: int, emulation_env_config: EmulationEnvAgentConfig, env_state: EmulationEnvState) -> bool:
        """
        Checks if a given defense action is legal in the current state of the environment

        :param defense_action_id: the id of the action to check
        :param emulation_env_config: the environment config
        :param env_state: the environment state
        :param attacker_action: the id of the previous attack action
        :return: True if legal, else false
        """
        return EnvUtil.is_defense_action_legal(defense_action_id=defense_action_id, env_config=emulation_env_config,
                                               env_state=env_state)

    @staticmethod
    def is_attack_action_legal(attack_action_id : int, emulation_env_config: EmulationEnvAgentConfig, env_state: EmulationEnvState) -> bool:
        """
        Checks if a given attack action is legal in the current state of the environment

        :param attack_action_id: the id of the action to check
        :param emulation_env_config: the environment config
        :param env_state: the environment state
        :return: True if legal, else false
        """
        return EnvUtil.is_attack_action_legal(attack_action_id=attack_action_id, env_config=emulation_env_config,
                                              env_state=env_state)

    def close(self) -> None:
        """
        Closes the viewer (cleanup)
        :return: None
        """
        if self.viewer:
            self.viewer.close()
            self.viewer = None

    def cleanup(self) -> None:
        """
        Cleans up environment state. This method is particularly useful in emulation mode where there are
        SSH/Telnet/FTP... connections that should be cleaned up, as well as background threads.

        :return: None
        """
        self.env_state.cleanup()
        if self.emulation_env_config.emulation_config is not None:
            self.emulation_env_config.emulation_config.close_all_connections()

    def attacker_convert_ar_action(self, machine_idx, action_idx):
        """
        Converts an AR action id into a global action id

        :param machine_idx: the machine id
        :param action_idx: the action id
        :return: the global action id
        """
        key = (machine_idx, action_idx)
        print(self.emulation_env_config.attacker_action_conf.ar_action_converter)
        return self.emulation_env_config.attacker_action_conf.ar_action_converter[key]

    # -------- Private methods ------------

    def __update_log(self, action : AttackerAction) -> None:
        """
        Updates the log for rendering with a new action

        :param action: the new action to add to the log
        :return: None
        """
        tag = "-"
        if not action.subnet:
            if action.ips is not None:
                tag = ""
                for ip in action.ips:
                    tag += str(ip.rsplit(".", 1)[-1])
        else:
            tag = "*"
        self.attacker_render_state.env_log.add_entry(action.name + "[." + tag + "]")

    def __setup_viewer(self):
        """
        Setup for the viewer to use for rendering

        :return: None
        """
        from csle_common.rendering.viewer import Viewer
        script_dir = os.path.dirname(__file__)
        resource_path = os.path.join(script_dir, './rendering/frames/', constants.RENDERING.RESOURCES_DIR)
        self.emulation_env_config.render_config.resources_dir = resource_path
        self.viewer = Viewer(env_config=self.emulation_env_config, init_state=self.attacker_render_state)
        self.viewer.start()

    def __checkpoint_log(self) -> None:
        """
        Checkpoints the agent log for an episode

        :return: None
        """
        if not self.emulation_env_config.checkpoint_dir == None \
                and self.attacker_render_state.num_episodes % self.emulation_env_config.checkpoint_freq == 0:
            file_path = self.emulation_env_config.checkpoint_dir + "/ep_" + str(self.attacker_render_state.num_episodes) + "_agent.log"
            with open(file_path, "w") as outfile:
                outfile.write("\n".join(self.attacker_render_state.env_log.log))

    def __checkpoint_trajectories(self) -> None:
        """
        Checkpoints agent trajectories

        :return: None
        """
        if self.emulation_env_config.save_trajectories and not self.emulation_env_config.checkpoint_dir == None \
                and self.attacker_render_state.num_episodes % self.emulation_env_config.checkpoint_freq == 0:
            file_path = self.emulation_env_config.checkpoint_dir + "/ep_" + str(self.attacker_render_state.num_episodes) \
                        + "_trajectories.pickle"
            with open(file_path, "wb") as outfile:
                pickle.dump(self.attacker_trajectories, outfile, protocol=pickle.HIGHEST_PROTOCOL)
                self.attacker_trajectories = []

    def reset_state(self) -> None:
        """
        Resets the environment state

        :return: None
        """
        self.env_state.reset()

    @staticmethod
    def initialize_info_dict() -> dict:
        """
        Initialize the info dict

        :return: the dict with the initialized values
        """
        info = {}
        info[constants.INFO_DICT.INTRUSION_STATE] = 0
        return info