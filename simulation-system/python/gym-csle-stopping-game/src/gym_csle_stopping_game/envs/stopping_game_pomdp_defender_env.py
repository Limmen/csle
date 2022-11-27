from typing import Tuple, List
import gym
import numpy as np
from csle_common.dao.simulation_config.base_env import BaseEnv
from gym_csle_stopping_game.dao.stopping_game_defender_pomdp_config import StoppingGameDefenderPomdpConfig
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from csle_common.dao.training.policy import Policy
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.emulation_config.emulation_simulation_trace import EmulationSimulationTrace
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from gym_csle_stopping_game.envs.stopping_game_env import StoppingGameEnv
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil


class StoppingGamePomdpDefenderEnv(BaseEnv):
    """
    OpenAI Gym Env for the MDP of the defender when facing a static attacker
    """

    def __init__(self, config: StoppingGameDefenderPomdpConfig):
        """
        Initializes the environment

        :param config: the environment configuration
        :param attacker_strategy: the strategy of the static attacker
        """
        self.config = config
        self.stopping_game_env = gym.make(self.config.stopping_game_name, config=self.config.stopping_game_config)

        # Setup spaces
        self.observation_space = self.config.stopping_game_config.defender_observation_space()
        self.action_space = self.config.stopping_game_config.defender_action_space()

        # Setup static attacker strategy
        self.static_attacker_strategy = self.config.attacker_strategy

        # Setup Config
        self.viewer = None
        self.metadata = {
            'render.modes': ['human', 'rgb_array'],
            'video.frames_per_second': 50  # Video rendering speed
        }

        self.latest_attacker_obs = None
        # Reset
        self.reset()
        super().__init__()

    def step(self, a1: int) -> Tuple[np.ndarray, int, bool, dict]:
        """
        Takes a step in the environment by executing the given action

        :param a1: defender action
        :return: (obs, reward, done, info)
        """
        # Get attacker action from static strategy
        pi2 = np.array(self.static_attacker_strategy.stage_policy(self.latest_attacker_obs))
        a2 = StoppingGameUtil.sample_attacker_action(pi2=pi2, s=self.stopping_game_env.state.s)

        # Step the game
        o, r, d, info = self.stopping_game_env.step((a1, (pi2, a2)))
        self.latest_attacker_obs = o[1]
        defender_obs = o[0]

        return defender_obs, r[0], d, info

    def step_test(self, a1: int, sample_Z) -> Tuple[np.ndarray, int, bool, dict]:
        """
        Takes a step in the environment by executing the given action

        :param a1: defender action
        :return: (obs, reward, done, info)
        """
        # Get attacker action from static strategy
        pi2 = np.array(self.static_attacker_strategy.stage_policy(self.latest_attacker_obs))
        a2 = StoppingGameUtil.sample_attacker_action(pi2=pi2, s=self.stopping_game_env.state.s)

        # Step the game
        o, r, d, info = self.stopping_game_env.step_test((a1, (pi2, a2)), sample_Z=sample_Z)
        self.latest_attacker_obs = o[1]
        defender_obs = o[0]

        return defender_obs, r[0], d, info

    def reset(self, soft: bool = False) -> np.ndarray:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :return: initial observation
        """
        o = self.stopping_game_env.reset()
        self.latest_attacker_obs = o[1]
        defender_obs = o[0]
        return defender_obs

    def render(self, mode: str = 'human'):
        """
        Renders the environment.  Supported rendering modes: (1) human; and (2) rgb_array

        :param mode: the rendering mode
        :return: True (if human mode) otherwise an rgb array
        """
        raise NotImplementedError("Rendering is not implemented for this environment")

    def step_trace(self, trace: EmulationTrace, a1: int) -> Tuple[np.ndarray, int, bool, dict]:
        pi2 = np.array(self.static_attacker_strategy.stage_policy(self.latest_attacker_obs))
        o, r, d, info = self.stopping_game_env.step_trace(trace=trace, a1=a1, pi2=pi2)
        self.latest_attacker_obs = o[1]
        defender_obs = o[0]
        return defender_obs, r[0], d, info

    @staticmethod
    def emulation_evaluation(env: "StoppingGamePomdpDefenderEnv",
                             n_episodes: int, intrusion_seq: List[EmulationAttackerAction],
                             defender_policy: Policy,
                             emulation_env_config: EmulationEnvConfig, simulation_env_config: SimulationEnvConfig) \
            -> List[EmulationSimulationTrace]:
        return StoppingGameEnv.emulation_evaluation(
            env=env.stopping_game_env, n_episodes=n_episodes, intrusion_seq=intrusion_seq,
            defender_policy=defender_policy, attacker_policy=env.static_attacker_strategy,
            emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config)

    def is_defense_action_legal(self, defense_action_id: int) -> bool:
        """
        Checks whether a defender action in the environment is legal or not

        :param defense_action_id: the id of the action
        :return: True or False
        """
        return True

    def is_attack_action_legal(self, attack_action_id: int) -> bool:
        """
        Checks whether an attacker action in the environment is legal or not

        :param attack_action_id: the id of the attacker action
        :return: True or False
        """
        return True

    def get_traces(self) -> List[SimulationTrace]:
        """
        :return: the list of simulation traces
        """
        return self.stopping_game_env.get_traces()

    def reset_traces(self) -> None:
        """
        Resets the list of traces

        :return: None
        """
        return self.stopping_game_env.reset_traces()

    def close(self) -> None:
        """
        Closes the viewer (cleanup)
        :return: None
        """
        if self.viewer:
            self.viewer.close()
            self.viewer = None

    def manual_play(self) -> None:
        """
        An interactive loop to test the environment manually

        :return: None
        """
        done = False
        while True:
            raw_input = input("> ")
            raw_input = raw_input.strip()
            if raw_input == "help":
                print("Enter an action id to execute the action, "
                      "press R to reset,"
                      "press S to print the state, press A to print the actions, "
                      "press D to check if done"
                      "press H to print the history of actions")
            elif raw_input == "A":
                print(f"Action space: {self.action_space}")
            elif raw_input == "S":
                print(self.stopping_game_env.state)
            elif raw_input == "D":
                print(done)
            elif raw_input == "H":
                print(self.stopping_game_env.trace)
            elif raw_input == "R":
                print("Resetting the state")
                self.reset()
            else:
                action_idx = int(raw_input)
                _, _, done, _ = self.step(pi2=action_idx)
