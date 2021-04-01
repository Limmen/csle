import numpy as np
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.network_config import NetworkConfig
from gym_pycr_ctf.envs_model.logic.exploration.exploration_policy import ExplorationPolicy
from gym_pycr_ctf.envs_model.logic.common.env_dynamics_util import EnvDynamicsUtil
from gym_pycr_ctf.dao.defender_dynamics.defender_dynamics_model import DefenderDynamicsModel

class SimulationGenerator:
    """
    Class for with functions for running an exploration policy in an environment to build a level_1 model
    that later can be used for simulations
    """

    @staticmethod
    def explore(attacker_exp_policy: ExplorationPolicy, env_config: EnvConfig, env,
                render: bool = False, defender_dynamics_model: DefenderDynamicsModel = None
                ) -> np.ndarray:
        """
        Explores the environment to generate trajectories that can be used to learn a dynamics model

        :param attacker_exp_policy: the exploration policy to use
        :param env_config: the env config
        :param env: the env to explore
        :param render: whether to render the env or not
        :param explore_defense_states: boolean flag whether to explore defensive states or not
        :return: The final observation
        """
        obs = env.reset()
        done = False
        step = 0
        if not env_config.explore_defense_states:
            defender_action = None
        else:
            defender_action = env_config.defender_action_conf.get_continue_action_idx()
        while not done and step < env_config.attacker_max_exploration_steps:

            # Sample action
            attacker_action = attacker_exp_policy.action(
                env=env, filter_illegal=env_config.attacker_exploration_filter_illegal)

            # Step in the environment
            action = (attacker_action, defender_action)
            obs_prime, reward, done, info = env.step(action)

            # Update dynamics
            if env_config.explore_defense_states and defender_dynamics_model is not None:
                attack_action_dto = env_config.attacker_action_conf.actions[attacker_action]
                logged_in_ips_str = EnvDynamicsUtil.logged_in_ips_str(env_config=env_config, a=attack_action_dto,
                                                                      s=env.env_state)
                defender_dynamics_model.update_model(obs=obs, obs_prime=obs_prime,
                                                     attacker_action_id=attack_action_dto.id,
                                                     logged_in_ips=logged_in_ips_str)

            # Move to next state
            obs= obs_prime

            step +=1
            if render:
                env.render()
        if step >= env_config.attacker_max_exploration_steps:
            print("maximum exploration steps reached")
        return defender_dynamics_model

    @staticmethod
    def build_model(exp_policy: ExplorationPolicy, env_config: EnvConfig, env, render: bool = False) -> NetworkConfig:
        print("Starting Exploration Phase to Gather Data to Create Simulation")
        aggregated_observation = env.env_state.attacker_obs_state.copy()
        defender_dynamics_model = SimulationGenerator.initialize_defender_dynamics_model()
        for i in range(env_config.attacker_max_exploration_trajectories):
            print("Collecting trajectory {}/{}".format(i, env_config.attacker_max_exploration_trajectories))
            defender_dynamics_model = \
                SimulationGenerator.explore(attacker_exp_policy= exp_policy, env_config=env_config,
                                            env=env, render=render, defender_dynamics_model=defender_dynamics_model)
            observation = env.env_state.attacker_obs_state
            aggregated_observation = EnvDynamicsUtil.merge_complete_obs_state(old_obs_state=aggregated_observation,
                                                                              new_obs_state=observation,
                                                                              env_config=env_config)
        num_machines = len(aggregated_observation.machines)
        num_vulnerabilities = sum(list(map(lambda x: len(x.cve_vulns) + len(x.osvdb_vulns), aggregated_observation.machines)))
        num_credentials = sum(list(map(lambda x: len(x.shell_access_credentials), aggregated_observation.machines)))
        print("Exploration completed, found {} machines, {} vulnerabilities, {} credentials".format(
            num_machines, num_vulnerabilities, num_credentials))
        print("Defender Dynamics Model:\n{}".format(defender_dynamics_model))
        nodes = list(map(lambda x: x.to_node(), aggregated_observation.machines))
        env_config.network_conf.nodes = nodes
        env_config.network_conf.defender_dynamics_model = defender_dynamics_model
        env_config.network_conf.agent_reachable = aggregated_observation.agent_reachable
        env.cleanup()
        return env_config.network_conf, aggregated_observation

    @staticmethod
    def initialize_defender_dynamics_model():
        defender_dynamics_model = DefenderDynamicsModel()
        return defender_dynamics_model