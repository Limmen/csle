from typing import Tuple
import numpy as np
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.dao.stopping_game_state import StoppingGameState


class StoppingGameEnv(BaseEnv):
    """
    OpenAI Gym Env for the csle-stopping-game
    """

    def __init__(self, config: StoppingGameConfig):
        self.config = config

        # Initialize environment state
        self.state = StoppingGameState(b1=self.config.b1, L=self.config.L)

        # Setup spaces
        self.attacker_observation_space = self.config.attacker_observation_space()
        self.defender_observation_space = self.config.defender_observation_space()
        self.attacker_action_space = self.config.attacker_action_space()
        self.defender_action_space = self.config.defender_action_space()

        # Setup Config
        self.viewer = None
        self.metadata = {
            'render.modes': ['human', 'rgb_array'],
            'video.frames_per_second': 50  # Video rendering speed
        }

        # Setup traces
        self.traces = []
        self.trace = SimulationTrace(simulation_env=self.unwrapped.spec.id)

        # Reset
        self.reset()
        super().__init__()

    def step(self, action_profile : Tuple[int, np.ndarray]) \
            -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[int, int], bool, dict]:
        """
        Takes a step in the environment by executing the given action

        :param action_profile: the actions to take (both players actions
        :return: (obs, reward, done, info)
        """

        # Setup initial values
        a1, pi2 = action_profile
        assert pi2.shape[0] == len(self.config.S)
        assert pi2.shape[1] == len(self.config.A1)
        done = False
        info = {}

        # Compute r, s', b',o'
        a2 = StoppingGameUtil.sample_attacker_action(pi2 = pi2, s=self.state.s)
        r = self.config.R[self.state.l - 1][a1][a2][self.state.s]
        self.state.s = StoppingGameUtil.sample_next_state(l=self.state.l, a1=a1, a2=a2,
                                                          T=self.config.T,
                                                          S=self.config.S, s=self.state.s)
        o = max(self.config.O)
        if self.state.s == 2:
            done = True
        else:
            o = StoppingGameUtil.sample_next_observation(Z=self.config.Z,
                                                         O=self.config.O, s_prime=self.state.s)
            self.state.b = StoppingGameUtil.next_belief(o=o, a1=a1, b=self.state.b, pi2=pi2,
                                                        config=self.config,
                                                        l=self.state.l, a2=a2)

        # Update stops remaining
        self.state.l = self.state.l-a1

        # Get observations
        attacker_obs = self.state.attacker_observation()
        defender_obs = self.state.defender_observation()

        # Log trace
        self.trace.defender_rewards.append(r)
        self.trace.attacker_rewards.append(-r)
        self.trace.attacker_actions.append(a2)
        self.trace.defender_actions.append(a1)
        self.trace.infos.append(info)
        self.trace.states.append(self.state.s)
        self.trace.beliefs.append(self.state.b[1])
        self.trace.infrastructure_metrics.append(o)
        if not done:
            self.trace.attacker_observations.append(attacker_obs)
            self.trace.defender_observations.append(defender_obs)

        return (defender_obs, attacker_obs), (r,-r), done, info

    def reset(self, soft : bool = False) -> Tuple[np.ndarray, np.ndarray]:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :return: initial observation
        """
        self.state.reset()
        if len(self.trace .attacker_rewards) > 0:
            self.traces.append(self.trace)
        if len(self.traces) > 1 and len(self.traces) % 100 == 0:
            self.__checkpoint_traces()
        self.trace = SimulationTrace()
        attacker_obs = self.state.attacker_observation()
        defender_obs = self.state.defender_observation()
        self.trace.attacker_observations.append(attacker_obs)
        self.trace.defender_observations.append(defender_obs)
        return defender_obs, attacker_obs

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
        raise NotImplemented("Rendering is not implemented for this environment")

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

    def __checkpoint_traces(self) -> None:
        """
        Checkpoints agent traces
        :return: None
        """
        SimulationTrace.save_traces(traces_save_dir=self.config.save_dir,
                                    traces=self.traces, traces_file="taus.json")

