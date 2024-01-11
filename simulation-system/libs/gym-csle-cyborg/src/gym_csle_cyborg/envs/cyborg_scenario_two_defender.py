from typing import Tuple, Dict, List, Any, Union
import numpy as np
import numpy.typing as npt
import time
import inspect
from csle_cyborg.main import Main
from csle_cyborg.agents.simple_agents.b_line import B_lineAgent
from csle_cyborg.agents.wrappers.challenge_wrapper import ChallengeWrapper
import csle_common.constants.constants as constants
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
import gym_csle_cyborg.constants.constants as env_constants
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig


class CyborgScenarioTwoDefender(BaseEnv):
    """
    OpenAI Gym Env for CybORG scenario 2 from the defender's perspective
    """

    def __init__(self, config: CSLECyborgConfig):
        """
        Initializes the environment

        :param config: the environment configuration
        """
        self.config = config
        self.cyborg_scenario_config_path = str(inspect.getfile(Main))
        self.cyborg_scenario_config_path = (f"{self.cyborg_scenario_config_path[:-7]}"
                                            f"{env_constants.CYBORG.SCENARIO_CONFIGS_DIR}"
                                            f"{env_constants.CYBORG.SCENARIO_CONFIG_PREFIX}{config.scenario}"
                                            f"{env_constants.CYBORG.SCENARIO_CONFIG_SUFFIX}")
        cyborg = Main(self.cyborg_scenario_config_path, env_constants.CYBORG.SIMULATION, agents={
            env_constants.CYBORG.RED: B_lineAgent
        })
        self.cyborg_challenge_env = ChallengeWrapper(env=cyborg, agent_name=env_constants.CYBORG.BLUE)

        # Setup spaces
        self.defender_observation_space = self.cyborg_challenge_env.observation_space
        self.defender_action_space = self.cyborg_challenge_env.action_space

        self.action_space = self.defender_action_space
        self.observation_space = self.defender_observation_space

        # Setup traces
        self.traces: List[SimulationTrace] = []
        self.trace = SimulationTrace(simulation_env=self.config.env_name)

        # Reset
        self.reset()
        super().__init__()

    def step(self, action: int) -> Tuple[npt.NDArray[Any], float, bool, bool, Dict[str, Any]]:
        """
        Takes a step in the environment by executing the given action

        :param action_profile: the actions to take (both players actions
        :return: (obs, reward, terminated, truncated, info)
        """
        o, r, done, _, info = self.cyborg_challenge_env.step(action=action)
        return np.array(o), float(r), bool(done), bool(done), info

    def reset(self, seed: Union[None, int] = None, soft: bool = False, options: Union[Dict[str, Any], None] = None) \
            -> Tuple[npt.NDArray[Any], Dict[str, Any]]:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :param seed: the random seed
        :param soft: boolean flag indicating whether it is a soft reset or not
        :param options: optional configuration parameters
        :return: initial observation and info
        """
        super().reset(seed=seed)
        o, d = self.cyborg_challenge_env.reset()
        return np.array(o), dict(d)

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
        return self.traces

    def reset_traces(self) -> None:
        """
        Resets the list of traces

        :return: None
        """
        self.traces = []

    def __checkpoint_traces(self) -> None:
        """
        Checkpoints agent traces
        :return: None
        """
        ts = time.time()
        SimulationTrace.save_traces(traces_save_dir=constants.LOGGING.DEFAULT_LOG_DIR,
                                    traces=self.traces, traces_file=f"taus{ts}.json")

    def set_model(self, model) -> None:
        """
        Sets the model. Useful when using RL frameworks where the stage policy is not easy to extract

        :param model: the model
        :return: None
        """
        self.model = model

    def manual_play(self) -> None:
        """
        An interactive loop to test the environment manually

        :return: None
        """
        return None
