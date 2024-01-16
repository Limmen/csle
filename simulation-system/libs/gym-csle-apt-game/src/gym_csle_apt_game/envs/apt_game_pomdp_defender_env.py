from typing import Tuple, List, Dict, Any, Union
import numpy as np
import numpy.typing as npt
from csle_common.dao.simulation_config.base_env import BaseEnv
from gym_csle_apt_game.dao.apt_game_defender_pomdp_config import AptGameDefenderPomdpConfig
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from gym_csle_apt_game.envs.apt_game_env import AptGameEnv
from gym_csle_apt_game.util.apt_game_util import AptGameUtil


class AptGamePomdpDefenderEnv(BaseEnv):
    """
    OpenAI Gym Env for the MDP of the defender when facing a static attacker
    """

    def __init__(self, config: AptGameDefenderPomdpConfig):
        """
        Initializes the environment

        :param config: the environment configuration
        :param attacker_strategy: the strategy of the static attacker
        """
        self.config = config
        self.apt_game_env = AptGameEnv(config=self.config.apt_game_config)

        # Setup spaces
        self.observation_space = self.config.apt_game_config.defender_observation_space()
        self.action_space = self.config.apt_game_config.defender_action_space()

        # Setup static attacker strategy
        self.static_attacker_strategy = self.config.attacker_strategy

        # Setup Config
        self.viewer: Union[None, Any] = None
        self.metadata = {
            'render.modes': ['human', 'rgb_array'],
            'video.frames_per_second': 50  # Video rendering speed
        }

        self.latest_attacker_obs: Union[None, Tuple[npt.NDArray[Any], int]] = None
        # Reset
        self.reset()
        super().__init__()

    def step(self, a1: int) -> Tuple[npt.NDArray[Any], float, bool, bool, Dict[str, Any]]:
        """
        Takes a step in the environment by executing the given action

        :param a1: defender action
        :return: (obs, reward, terminated, truncated, info)
        """
        # Get attacker action from static strategy
        pi2 = np.array(self.static_attacker_strategy.stage_policy(self.latest_attacker_obs))
        a2 = AptGameUtil.sample_attacker_action(pi2=pi2, s=self.apt_game_env.state.s)

        # Step the game
        o, r, d, _, info = self.apt_game_env.step((a1, (pi2, a2)))
        self.latest_attacker_obs = o[1]
        defender_obs = o[0]
        defender_obs = np.array([1, sum(defender_obs[1:])])
        return defender_obs, float(r[0]), d, d, info

    def reset(self, seed: Union[None, int] = None, soft: bool = False, options: Union[Dict[str, Any], None] = None) \
            -> Tuple[npt.NDArray[Any], Dict[str, Any]]:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :param seed: the random seed
        :param soft: boolean flag indicating whether it is a soft reset or not
        :param options: optional configuration parameters
        :return: initial observation
        """
        o, _ = self.apt_game_env.reset()
        self.latest_attacker_obs = o[1]
        defender_obs = o[0]
        defender_obs_prime = np.array([1, sum(defender_obs[1:])])
        dict: Dict[str, Any] = {}
        return defender_obs_prime, dict

    def render(self, mode: str = 'human'):
        """
        Renders the environment.  Supported rendering modes: (1) human; and (2) rgb_array

        :param mode: the rendering mode
        :return: True (if human mode) otherwise an rgb array
        """
        raise NotImplementedError("Rendering is not implemented for this environment")

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
        return self.apt_game_env.get_traces()

    def reset_traces(self) -> None:
        """
        Resets the list of traces

        :return: None
        """
        return self.apt_game_env.reset_traces()

    def set_model(self, model) -> None:
        """
        Sets the model. Useful when using RL frameworks where the stage policy is not easy to extract

        :param model: the model
        :return: None
        """
        self.model = model

    def set_state(self, state: Any) -> None:
        """
        Sets the state. Allows to simulate samples from specific states

        :param state: the state
        :return: None
        """
        self.apt_game_env.set_state(state=state)

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
                print(self.apt_game_env.state)
            elif raw_input == "D":
                print(done)
            elif raw_input == "H":
                print(self.apt_game_env.trace)
            elif raw_input == "R":
                print("Resetting the state")
                self.reset()
            else:
                action_idx = int(raw_input)
                _, _, done, _, _ = self.step(a1=action_idx)
