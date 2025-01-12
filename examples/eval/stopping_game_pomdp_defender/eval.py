import gymnasium as gym
import csle_common.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy
from gym_csle_stopping_game.envs.stopping_game_pomdp_defender_env import StoppingGamePomdpDefenderEnv
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.training.agent_type import AgentType


def test_env() -> None:
    """
    Runs a test environment

    :return: None
    """
    emulation_env_config = MetastoreFacade.get_emulation_by_name("csle-level9-070")
    simulation_env_config = MetastoreFacade.get_simulation_by_name("csle-stopping-pomdp-defender-002")
    config = simulation_env_config.simulation_env_input_config
    env = gym.make(simulation_env_config.gym_env_name, config=config)
    tspsa_policy = MultiThresholdStoppingPolicy(theta=[0.9, 0.7, 0.5], simulation_name=simulation_env_config.name,
                                                states=simulation_env_config.state_space_config.states, L=3,
                                                player_type=PlayerType.DEFENDER,
                                                actions=simulation_env_config.joint_action_space_config.action_spaces[
                                                    0].actions,
                                                experiment_config=None, avg_R=-1, agent_type=AgentType.NONE)

    StoppingGamePomdpDefenderEnv.emulation_evaluation(
        env=env, n_episodes=10,
        intrusion_seq=emulation_env_config.static_attacker_sequences[constants.STATIC_ATTACKERS.EXPERT],
        defender_policy=tspsa_policy, emulation_env_config=emulation_env_config,
        simulation_env_config=simulation_env_config
    )


if __name__ == '__main__':
    test_env()
