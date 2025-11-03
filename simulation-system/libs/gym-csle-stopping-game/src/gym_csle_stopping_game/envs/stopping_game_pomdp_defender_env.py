from typing import Tuple, List, Dict, Any, Union
import numpy as np
import numpy.typing as npt
from csle_common.dao.simulation_config.base_env import BaseEnv
from gym_csle_stopping_game.dao.stopping_game_defender_pomdp_config import StoppingGameDefenderPomdpConfig
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from gym_csle_stopping_game.envs.stopping_game_env import StoppingGameEnv
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil


class StoppingGamePomdpDefenderEnv(BaseEnv):
    """
    OpenAI Gym Env for the POMDP of the defender when facing a static attacker
    """

    def __init__(self, config: StoppingGameDefenderPomdpConfig):
        """
        Initializes the environment

        :param config: the environment configuration
        :param attacker_strategy: the strategy of the static attacker
        """
        self.config = config
        self.stopping_game_env = StoppingGameEnv(config=self.config.stopping_game_config)

        # Setup spaces
        self.observation_space = self.config.stopping_game_config.defender_observation_space()
        self.action_space = self.config.stopping_game_config.defender_action_space()

        # Setup static attacker strategy
        self.static_attacker_strategy = self.config.attacker_strategy

        # Setup Config
        self.viewer: Union[None, Any] = None
        self.metadata = {
            'render.modes': ['human', 'rgb_array'],
            'video.frames_per_second': 50  # Video rendering speed
        }

        self.latest_attacker_obs: Union[None, npt.NDArray[Any]] = None
        # Reset
        self.reset()
        super().__init__()

    def step(self, a1: int) -> Tuple[npt.NDArray[Any], int, bool, bool, Dict[str, Any]]:
        """
        Takes a step in the environment by executing the given action

        :param a1: defender action
        :return: (obs, reward, terminated, truncated, info)
        """
        # Get attacker action from static strategy
        pi2 = np.array(self.static_attacker_strategy.stage_policy(self.latest_attacker_obs))
        a2 = StoppingGameUtil.sample_attacker_action(pi2=pi2, s=self.stopping_game_env.state.s)
        # Step the game
        o, r, d, _, info = self.stopping_game_env.step((a1, (pi2, a2)))
        self.latest_attacker_obs = o[1]
        defender_obs = o[0]

        return defender_obs, r[0], d, d, info

    def reset(self, seed: Union[None, int] = None, soft: bool = False, options: Union[Dict[str, Any], None] = None) \
            -> Tuple[npt.NDArray[Any], Dict[str, Any]]:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :param seed: the random seed
        :param soft: boolean flag indicating whether it is a soft reset or not
        :param options: optional configuration parameters
        :return: initial observation
        """
        o, info = self.stopping_game_env.reset()
        self.latest_attacker_obs = o[1]
        defender_obs = o[0]
        return defender_obs, info

    def render(self, mode: str = 'human'):
        """
        Renders the environment.  Supported rendering modes: (1) human; and (2) rgb_array

        :param mode: the rendering mode
        :return: True (if human mode) otherwise an rgb array
        """
        raise NotImplementedError("Rendering is not implemented for this environment")

    def step_trace(self, trace: EmulationTrace, a1: int) -> Tuple[npt.NDArray[Any], int, bool, Dict[str, Any]]:
        """
        Utility method for stopping a pre-recorded trace

        :param trace: the trace to step
        :param a1: the action to step with
        :return: the result of the step according to the trace
        """
        pi2 = np.array(self.static_attacker_strategy.stage_policy(self.latest_attacker_obs))
        o, r, d, info = self.stopping_game_env.step_trace(trace=trace, a1=a1, pi2=pi2)
        self.latest_attacker_obs = o[1]
        defender_obs = o[0]
        return defender_obs, r[0], d, info

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
        self.stopping_game_env.set_state(state=state)

    def get_observation_from_history(self, history: List[int]) -> List[Any]:
        """
        Utiltiy function to get a defender observation (belief) from a history

        :param history: the history to get the observation form
        :return: the observation
        """
        l = self.config.stopping_game_config.L
        return self.stopping_game_env.get_observation_from_history(
            history=history, pi2=self.static_attacker_strategy.stage_policy(o=0), l=l)

    def is_state_terminal(self, state: Any) -> bool:
        """
        Utility funciton to check whether a state is terminal or not

        :param state: the state
        :return: None
        """
        return self.stopping_game_env.is_state_terminal(state=state)

    def add_observation_vector(self, obs_vector: List[Any], obs_id: int) -> None:
        """
        Adds an observation vector to the history

        :param obs_vector: the observation vector to add
        :param obs_id: the id of the observation
        :return: None
        """
        pass

    def generate_random_particles(self, o: int, num_particles: int) -> List[int]:
        """
        Generates a random list of state particles from a given observation

        :param o: the latest observation
        :param num_particles: the number of particles to generate
        :return: the list of random particles
        """
        return self.stopping_game_env.generate_random_particles(o=o, num_particles=num_particles)

    def get_actions_from_particles(self, particles: List[int], t: int, observation: int,
                                   verbose: bool = False) -> List[int]:
        """
        Prunes the set of actiosn based on the current particle set

        :param particles: the set of particles
        :param t: the current time step
        :param observation: the latest observation
        :param verbose: boolean flag indicating whether logging should be verbose or not
        :return: the list of pruned actions
        """
        return list(self.config.stopping_game_config.A1)

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
                _, _, done, _, _ = self.step(a1=action_idx)
