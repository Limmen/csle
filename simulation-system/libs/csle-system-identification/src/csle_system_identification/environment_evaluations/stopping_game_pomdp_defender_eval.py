from typing import List
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.training.policy import Policy
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.emulation_config.emulation_simulation_trace import EmulationSimulationTrace
from gym_csle_stopping_game.envs.stopping_game_pomdp_defender_env import StoppingGamePomdpDefenderEnv
from csle_system_identification.environment_evaluations.stopping_game_emulation_eval import StoppingGameEmulationEval


class StoppingGamePomdpDefenderEval:
    """
    Utility class for performing emulation evaluations of the defender POMDP
    """

    @staticmethod
    def emulation_evaluation(env: StoppingGamePomdpDefenderEnv,
                             n_episodes: int, intrusion_seq: List[EmulationAttackerAction],
                             defender_policy: Policy,
                             emulation_env_config: EmulationEnvConfig, simulation_env_config: SimulationEnvConfig) \
            -> List[EmulationSimulationTrace]:
        """
        Utility function for evaluating policies in the emulation environment

        :param env: the environment to use for evaluation
        :param n_episodes: the number of episodes to use for evaluation
        :param intrusion_seq: the sequence of intrusion actions to use for evaluation
        :param defender_policy: the defender policy to use for evaluation
        :param emulation_env_config: the configuration of the emulation environment to use for evaluation
        :param simulation_env_config: the configuration of the simulation environment to use for evaluation
        :return: traces with the evaluation results
        """
        return StoppingGameEmulationEval.emulation_evaluation(
            env=env.stopping_game_env, n_episodes=n_episodes, intrusion_seq=intrusion_seq,
            defender_policy=defender_policy, attacker_policy=env.static_attacker_strategy,
            emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config)
