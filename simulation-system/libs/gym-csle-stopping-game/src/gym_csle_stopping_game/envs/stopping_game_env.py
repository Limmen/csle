from typing import Tuple, Dict, List, Any, Union
import numpy as np
import numpy.typing as npt
import time
import math
import csle_common.constants.constants as constants
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from csle_common.dao.training.policy import Policy
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.emulation_config.emulation_simulation_trace import EmulationSimulationTrace
from csle_common.dao.emulation_action.attacker.emulation_attacker_stopping_actions \
    import EmulationAttackerStoppingActions
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_stopping_actions \
    import EmulationDefenderStoppingActions
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.logging.log import Logger
from csle_system_identification.emulator import Emulator
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.dao.stopping_game_state import StoppingGameState
import gym_csle_stopping_game.constants.constants as env_constants
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType


class StoppingGameEnv(BaseEnv):
    """
    OpenAI Gym Env for the csle-stopping-game
    """

    def __init__(self, config: StoppingGameConfig):
        """
        Initializes the environment

        :param config: the environment configuration
        """
        self.config = config

        # Initialize environment state
        self.state = StoppingGameState(b1=self.config.b1, L=self.config.L)

        # Setup spaces
        self.attacker_observation_space = self.config.attacker_observation_space()
        self.defender_observation_space = self.config.defender_observation_space()
        self.attacker_action_space = self.config.attacker_action_space()
        self.defender_action_space = self.config.defender_action_space()

        self.action_space = self.defender_action_space
        self.observation_space = self.defender_observation_space

        # Setup traces
        self.traces: List[SimulationTrace] = []
        self.trace = SimulationTrace(simulation_env=self.config.env_name)

        # Reset
        self.reset()
        super().__init__()

    def step(self, action_profile: Tuple[int, Tuple[npt.NDArray[Any], int]]) \
            -> Tuple[Tuple[npt.NDArray[Any], npt.NDArray[Any]], Tuple[int, int], bool, bool, Dict[str, Any]]:
        """
        Takes a step in the environment by executing the given action

        :param action_profile: the actions to take (both players actions
        :return: (obs, reward, terminated, truncated, info)
        """

        # Setup initial values
        a1, a2_profile = action_profile
        pi2, a2 = a2_profile
        assert pi2.shape[0] == len(self.config.S)
        assert pi2.shape[1] == len(self.config.A1)
        done = False
        info: Dict[str, Any] = {}

        # Compute r, s', b',o'
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
        self.state.l = self.state.l - a1

        # Update time-step
        self.state.t += 1

        # Populate info dict
        info[env_constants.ENV_METRICS.STOPS_REMAINING] = self.state.l
        info[env_constants.ENV_METRICS.STATE] = self.state.s
        info[env_constants.ENV_METRICS.DEFENDER_ACTION] = a1
        info[env_constants.ENV_METRICS.ATTACKER_ACTION] = a2
        info[env_constants.ENV_METRICS.OBSERVATION] = o
        info[env_constants.ENV_METRICS.TIME_STEP] = self.state.t

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

        # Populate info
        info = self._info(info)

        return (defender_obs, attacker_obs), (r, -r), done, done, info

    def step_test(self, action_profile: Tuple[int, Tuple[npt.NDArray[Any], int]], sample_Z) \
            -> Tuple[Tuple[npt.NDArray[Any], npt.NDArray[Any]], Tuple[int, int], bool, Dict[str, Any]]:
        """
        Takes a step in the environment by executing the given action

        :param action_profile: the actions to take (both players actions
        :return: (obs, reward, done, info)
        """

        # Setup initial values
        a1, a2_profile = action_profile
        pi2, a2 = a2_profile
        assert pi2.shape[0] == len(self.config.S)
        assert pi2.shape[1] == len(self.config.A1)
        done = False
        info: Dict[str, Any] = {}

        # Compute r, s', b',o'
        r = self.config.R[self.state.l - 1][a1][a2][self.state.s]
        self.state.s = StoppingGameUtil.sample_next_state(l=self.state.l, a1=a1, a2=a2,
                                                          T=self.config.T,
                                                          S=self.config.S, s=self.state.s)
        o = max(self.config.O)
        if self.state.s == 2:
            done = True
        else:
            o = StoppingGameUtil.sample_next_observation(Z=sample_Z,
                                                         O=self.config.O, s_prime=self.state.s)
            self.state.b = StoppingGameUtil.next_belief(o=o, a1=a1, b=self.state.b, pi2=pi2,
                                                        config=self.config,
                                                        l=self.state.l, a2=a2)
        # Update stops remaining
        self.state.l = self.state.l - a1

        # Update time-step
        self.state.t += 1

        # Populate info dict
        info[env_constants.ENV_METRICS.STOPS_REMAINING] = self.state.l
        info[env_constants.ENV_METRICS.STATE] = self.state.s
        info[env_constants.ENV_METRICS.DEFENDER_ACTION] = a1
        info[env_constants.ENV_METRICS.ATTACKER_ACTION] = a2
        info[env_constants.ENV_METRICS.OBSERVATION] = o
        info[env_constants.ENV_METRICS.TIME_STEP] = self.state.t

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

        # Populate info
        info = self._info(info)

        return (defender_obs, attacker_obs), (r, -r), done, info

    def step_trace(self, trace: EmulationTrace, a1: int, pi2: npt.NDArray[Any]) \
            -> Tuple[Tuple[npt.NDArray[Any], npt.NDArray[Any]], Tuple[int, int], bool, Dict[str, Any]]:
        """
        Utility function for stepping a given trace

        :param trace: the trace to step
        :param a1: the action to step with
        :param pi2: the policy of the attacker
        :return: the result of the step
        """
        done = False
        info: Dict[str, Any] = {}
        if (self.state.t - 1) < len(trace.attacker_actions):
            a2_emulation_action = trace.attacker_actions[self.state.t - 1]
            a2 = 0
            if a2_emulation_action.type != EmulationAttackerActionType.CONTINUE and self.state.s == 0:
                a2 = 1
            if self.state.s == 1:
                a2 = 0
            # Compute r, s', b',o'
            r = self.config.R[self.state.l - 1][a1][a2][self.state.s]
            self.state.s = StoppingGameUtil.sample_next_state(l=self.state.l, a1=a1, a2=a2,
                                                              T=self.config.T,
                                                              S=self.config.S, s=self.state.s)
            o = max(self.config.O)
            if self.state.s == 2:
                done = True
            else:
                o = trace.defender_observation_states[self.state.t - 1].avg_snort_ids_alert_counters.warning_alerts
                if o >= len(self.config.O):
                    o = len(self.config.O) - 1
                self.state.b = StoppingGameUtil.next_belief(o=o, a1=a1, b=self.state.b, pi2=pi2,
                                                            config=self.config,
                                                            l=self.state.l, a2=a2)

            # Update stops remaining
            self.state.l = self.state.l - a1
        else:
            self.state.s = 2
            done = True
            a2 = 0
            o = 0
            r = 0

        # Update time-step
        self.state.t += 1

        # Populate info dict
        info[env_constants.ENV_METRICS.STOPS_REMAINING] = self.state.l
        info[env_constants.ENV_METRICS.STATE] = self.state.s
        info[env_constants.ENV_METRICS.DEFENDER_ACTION] = a1
        info[env_constants.ENV_METRICS.ATTACKER_ACTION] = a2
        info[env_constants.ENV_METRICS.OBSERVATION] = o
        info[env_constants.ENV_METRICS.TIME_STEP] = self.state.t

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
        info = self._info(info)
        return (defender_obs, attacker_obs), (r, -r), done, info

    def mean(self, prob_vector):
        """
        Utility function for getting the mean of a vector

        :param prob_vector: the vector to take the mean of
        :return: the mean
        """
        m = 0
        for i in range(len(prob_vector)):
            m += prob_vector[i] * i
        return m

    def weighted_intrusion_prediction_distance(self, intrusion_start: int, first_stop: int):
        """
        Computes the weighted intrusion start time prediction distance (Wang, Hammar, Stadler, 2022)

        :param intrusion_start: the intrusion start time
        :param first_stop: the predicted start time
        :return: the weighted distance
        """
        if first_stop <= intrusion_start:
            return 1 - (10 / 10)
        else:
            return 1 - (min(10, (first_stop - (intrusion_start + 1))) / 2) / 10

    def _info(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adds the cumulative reward and episode length to the info dict

        :param info: the info dict to update
        :return: the updated info dict
        """
        R = 0
        for i in range(len(self.trace.defender_rewards)):
            R += self.trace.defender_rewards[i] * math.pow(self.config.gamma, i)
        info[env_constants.ENV_METRICS.RETURN] = sum(self.trace.defender_rewards)
        info[env_constants.ENV_METRICS.TIME_HORIZON] = len(self.trace.defender_actions)
        stop = self.config.L
        for i in range(1, self.config.L + 1):
            info[f"{env_constants.ENV_METRICS.STOP}_{i}"] = len(self.trace.states)
        for i in range(len(self.trace.defender_actions)):
            if self.trace.defender_actions[i] == 1:
                info[f"{env_constants.ENV_METRICS.STOP}_{stop}"] = i
                stop -= 1
        intrusion_start = len(self.trace.defender_actions)
        for i in range(len(self.trace.attacker_actions)):
            if self.trace.attacker_actions[i] == 1:
                intrusion_start = i
                break
        intrusion_end = len(self.trace.attacker_actions)
        info[env_constants.ENV_METRICS.INTRUSION_START] = intrusion_start
        info[env_constants.ENV_METRICS.INTRUSION_END] = intrusion_end
        info[env_constants.ENV_METRICS.START_POINT_CORRECT] = \
            int(intrusion_start == (info[f"{env_constants.ENV_METRICS.STOP}_1"] + 1))
        info[env_constants.ENV_METRICS.WEIGHTED_INTRUSION_PREDICTION_DISTANCE] = \
            self.weighted_intrusion_prediction_distance(intrusion_start=intrusion_start,
                                                        first_stop=info[f"{env_constants.ENV_METRICS.STOP}_1"])
        info[env_constants.ENV_METRICS.INTRUSION_LENGTH] = intrusion_end - intrusion_start
        upper_bound_return = 0
        defender_baseline_stop_on_first_alert_return = 0
        upper_bound_stops_remaining = self.config.L
        defender_baseline_stop_on_first_alert_stops_remaining = self.config.L
        for i in range(len(self.trace.states)):
            if defender_baseline_stop_on_first_alert_stops_remaining > 0:
                if self.trace.infrastructure_metrics[i] > 0:
                    defender_baseline_stop_on_first_alert_return += \
                        self.config.R[int(defender_baseline_stop_on_first_alert_stops_remaining) - 1][1][
                            self.trace.attacker_actions[i]][self.trace.states[i]] * math.pow(self.config.gamma, i)
                    defender_baseline_stop_on_first_alert_stops_remaining -= 1
                else:
                    defender_baseline_stop_on_first_alert_return += \
                        self.config.R[int(defender_baseline_stop_on_first_alert_stops_remaining) - 1][0][
                            self.trace.attacker_actions[i]][self.trace.states[i]] * math.pow(self.config.gamma, i)
            if upper_bound_stops_remaining > 0:
                if self.trace.states[i] == 0:
                    r = self.config.R[int(upper_bound_stops_remaining) - 1][0][self.trace.attacker_actions[i]][
                        self.trace.states[i]]
                    upper_bound_return += r * math.pow(self.config.gamma, i)
                else:
                    r = self.config.R[int(upper_bound_stops_remaining) - 1][1][self.trace.attacker_actions[i]][
                        self.trace.states[i]]
                    upper_bound_return += r * math.pow(self.config.gamma, i)
                    upper_bound_stops_remaining -= 1
        info[env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN] = upper_bound_return
        info[env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN] = \
            defender_baseline_stop_on_first_alert_return
        return info

    def reset(self, seed: Union[None, int] = None, soft: bool = False, options: Union[Dict[str, Any], None] = None) \
            -> Tuple[Tuple[npt.NDArray[Any], npt.NDArray[Any]], Dict[str, Any]]:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :param seed: the random seed
        :param soft: boolean flag indicating whether it is a soft reset or not
        :param options: optional configuration parameters
        :return: initial observation and info
        """
        super().reset(seed=seed)
        self.state.reset()
        if len(self.trace.attacker_rewards) > 0:
            self.traces.append(self.trace)
        self.trace = SimulationTrace(simulation_env=self.config.env_name)
        attacker_obs = self.state.attacker_observation()
        defender_obs = self.state.defender_observation()
        self.trace.attacker_observations.append(attacker_obs)
        self.trace.defender_observations.append(defender_obs)
        info: Dict[str, Any] = {}
        return (defender_obs, attacker_obs), info

    @staticmethod
    def emulation_evaluation(env: "StoppingGameEnv", n_episodes: int, intrusion_seq: List[EmulationAttackerAction],
                             defender_policy: Policy,
                             attacker_policy: Policy,
                             emulation_env_config: EmulationEnvConfig,
                             simulation_env_config: SimulationEnvConfig
                             ) -> List[EmulationSimulationTrace]:
        """
        Utility function for evaluating a strategy profile in the emulation environment

        :param env: the environment to use for evaluation
        :param n_episodes: the number of evaluation episodes
        :param intrusion_seq: the intrusion sequence for the evaluation (sequence of attacker actions)
        :param defender_policy: the defender policy for the evaluation
        :param attacker_policy: the attacker policy for the evaluation
        :param emulation_env_config: configuration of the emulation environment for the evaluation
        :param simulation_env_config: configuration of the simulation environment for the evaluation
        :return: traces with the evaluation results
        """
        logger = Logger.__call__().get_logger()
        traces = []
        s = EmulationEnvState(emulation_env_config=emulation_env_config)
        s.initialize_defender_machines()
        for i in range(n_episodes):
            done = False
            defender_obs_space = simulation_env_config.joint_observation_space_config.observation_spaces[0]
            b = env.state.b1
            o, _ = env.reset()
            (d_obs, a_obs) = o
            t = 0
            s.reset()
            emulation_trace = EmulationTrace(initial_attacker_observation_state=s.attacker_obs_state,
                                             initial_defender_observation_state=s.defender_obs_state,
                                             emulation_name=emulation_env_config.name)
            simulation_trace = SimulationTrace(simulation_env=env.config.env_name)
            while not done:
                a1 = defender_policy.action(d_obs)
                a2 = attacker_policy.action(a_obs)
                o, r, done, info, _ = env.step((a1, a2))
                (d_obs, a_obs) = o
                r_1, r_2 = r
                logger.debug(f"a1:{a1}, a2:{a2}, d_obs:{d_obs}, a_obs:{a_obs}, r:{r}, done:{done}, info: {info}")
                if a1 == 0:
                    defender_action = EmulationDefenderStoppingActions.CONTINUE(index=-1)
                else:
                    defender_action = EmulationDefenderStoppingActions.CONTINUE(index=-1)
                if env.state.s == 1:
                    if t >= len(intrusion_seq):
                        t = 0
                    attacker_action = intrusion_seq[t]
                else:
                    attacker_action = EmulationAttackerStoppingActions.CONTINUE(index=-1)
                print(f"emulation a1:{defender_action}, emulation a2:{attacker_action}")
                emulation_trace, s = Emulator.run_actions(
                    s=s,
                    emulation_env_config=emulation_env_config, attacker_action=attacker_action,
                    defender_action=defender_action, trace=emulation_trace,
                    sleep_time=emulation_env_config.kafka_config.time_step_len_seconds)
                o_components = [s.defender_obs_state.snort_ids_alert_counters.severe_alerts,
                                s.defender_obs_state.snort_ids_alert_counters.warning_alerts,
                                s.defender_obs_state.aggregated_host_metrics.num_failed_login_attempts]
                o_components_str = ",".join(list(map(lambda x: str(x), o_components)))
                logger.debug(f"o_components:{o_components}")
                logger.debug(f"observation_id_to_observation_vector_inv:"
                             f"{defender_obs_space.observation_id_to_observation_vector_inv}")
                logger.debug(f"observation_id_to_observation_vector_inv:"
                             f"{o_components_str in defender_obs_space.observation_id_to_observation_vector_inv}")
                emulation_o = 0
                if o_components_str in defender_obs_space.observation_id_to_observation_vector_inv:
                    emulation_o = defender_obs_space.observation_id_to_observation_vector_inv[o_components_str]
                logger.debug(f"o:{emulation_o}")
                b = StoppingGameUtil.next_belief(o=emulation_o, a1=a1, b=b, pi2=a2, config=env.config,
                                                 l=env.state.l, a2=a2)
                d_obs[1] = b[1]
                a_obs[1] = b[1]
                logger.debug(f"b:{b}")
                simulation_trace.defender_rewards.append(r_1)
                simulation_trace.attacker_rewards.append(r_2)
                simulation_trace.attacker_actions.append(a2)
                simulation_trace.defender_actions.append(a1)
                simulation_trace.infos.append(info)
                simulation_trace.states.append(s)
                simulation_trace.beliefs.append(b[1])
                simulation_trace.infrastructure_metrics.append(emulation_o)

            em_sim_trace = EmulationSimulationTrace(emulation_trace=emulation_trace, simulation_trace=simulation_trace)
            MetastoreFacade.save_emulation_simulation_trace(em_sim_trace)
            traces.append(em_sim_trace)
        return traces

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
                print(f"Attacker space: {self.action_space}")
            elif raw_input == "S":
                print(self.state)
            elif raw_input == "D":
                print(done)
            elif raw_input == "H":
                print(self.trace)
            elif raw_input == "R":
                print("Resetting the state")
                self.reset()
            else:
                action_profile = raw_input
                parts = action_profile.split(",")
                a1 = int(parts[0])
                a2 = int(parts[1])
                stage_policy = []
                for s in self.config.S:
                    if s != 2:
                        dist = [0.0, 0.0]
                        dist[a2] = 1.0
                        stage_policy.append(dist)
                    else:
                        stage_policy.append([0.5, 0.5])
                pi2 = np.array(stage_policy)
                _, _, done, _, _ = self.step(action_profile=(a1, (pi2, a2)))
