from typing import List
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.policy import Policy
from csle_common.dao.emulation_config.emulation_simulation_trace import EmulationSimulationTrace
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_action.defender.emulation_defender_stopping_actions import (
    EmulationDefenderStoppingActions)
from csle_common.dao.emulation_action.attacker.emulation_attacker_stopping_actions import (
    EmulationAttackerStoppingActions)
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.logging.log import Logger
from gym_csle_stopping_game.envs.stopping_game_env import StoppingGameEnv
from csle_system_identification.emulator import Emulator
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil


class StoppingGameEmulationEval:
    """
    Utility class for performing emulation evaluations of the stopping game
    """

    @staticmethod
    def emulation_evaluation(env: StoppingGameEnv, n_episodes: int, intrusion_seq: List[EmulationAttackerAction],
                             defender_policy: Policy, attacker_policy: Policy, emulation_env_config: EmulationEnvConfig,
                             simulation_env_config: SimulationEnvConfig) -> List[EmulationSimulationTrace]:
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
