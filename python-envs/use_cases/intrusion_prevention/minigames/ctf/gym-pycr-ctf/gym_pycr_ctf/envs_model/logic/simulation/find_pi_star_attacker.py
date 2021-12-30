from typing import Tuple
from pycr_common.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.network.env_config import PyCREnvConfig
from gym_pycr_ctf.envs_model.logic.transition_operator import TransitionOperator
from gym_pycr_ctf.dao.action.attacker.attacker_action_id import AttackerActionId


class FindPiStarAttacker:
    """
    Class with utility methods for finding pi-star for simple environments, can be used to
    evaluate learning performance
    """

    @staticmethod
    def brute_force(env_config: PyCREnvConfig, env) -> Tuple[list, float]:
        """
        Attempts to compute the optimal policy for the attacker using brute-force search

        :param env_config: the environment configuration
        :param env: the environment to compute pi-star for
        :return: (optimal tau, optimal r)
        """
        shortest_paths = env_config.network_conf.shortest_paths()
        if len(shortest_paths) == 0:
            return [], -1
        p = shortest_paths[0]
        paths = []
        pivot_actions = FindPiStarAttacker.pivot_actions(env_config=env_config)
        env.reset(soft=True)
        p = p[0]
        for n in p:
            for a in env_config.attacker_action_conf.actions:
                a.ip = env.env_state.attacker_obs_state.get_action_ip(a)
                s_prime, reward, done = TransitionOperator.attacker_transition(s=env.env_state, attacker_action=a, env_config=env_config)
                if n in list(map(lambda x: x.ip, s_prime.attacker_obs_state.machines)):
                    env.env_state = s_prime
                    r_nodes = p.copy()
                    r_nodes.remove(n)
                    next_node = n
                    paths = paths + FindPiStarAttacker._breach_node(path=[a], current_node=next_node, remaining_nodes=r_nodes,
                                                                    rew=reward, env=env, env_config=env_config,
                                                                    pivot_actions=pivot_actions)
                    env.reset(soft=True)
        sorted_paths = sorted(paths, key=lambda x: x[1])
        pi_star =sorted_paths[-1]
        return pi_star[0], pi_star[1]

    @staticmethod
    def _breach_node(path, current_node, remaining_nodes, rew, env, env_config, pivot_actions):
        """
        Helper function to compute pi-star

        :param path: the current path
        :param current_node: the current node
        :param remaining_nodes: remaining nodes
        :param rew: the current reward
        :param env: the env
        :param env_config: the environment configuration
        :param pivot_actions: list of actions that can be used for pivoting
        :return: List of (pi_star[0], pi_star[1])
        """
        paths = []
        shell_access = False
        old_state = env.env_state.copy()
        for k in env.env_state.attacker_obs_state.machines:
            if k.ip == current_node and k.shell_access:
                shell_access = True
        if not shell_access:
            for a in env_config.attacker_action_conf.actions:
                env.reset(soft=True)
                env.env_state = old_state.copy()
                k_path = path
                a_rew = rew
                a.ip = env.env_state.attacker_obs_state.get_action_ip(a)
                s_prime, reward, done = TransitionOperator.attacker_transition(s=env.env_state, attacker_action=a, env_config=env_config)
                for k in s_prime.attacker_obs_state.machines:
                    if k.ip == current_node:
                        if k.shell_access:
                            k_path = k_path + [a]
                            a_rew = a_rew + reward
                            env.env_state = s_prime
                            for a in pivot_actions:
                                a.ip = env.env_state.attacker_obs_state.get_action_ip(a)
                                s_prime, reward, done = TransitionOperator.attacker_transition(s=env.env_state, attacker_action=a,
                                                                                               env_config=env_config)
                                a_rew = reward + a_rew
                                k_path = k_path + [a]
                                env.env_state = s_prime
                                if done:
                                    paths.append((k_path, a_rew))

                            if not len(remaining_nodes) == 0 and not done:
                                old_state2 = env.env_state.copy()
                                for n in remaining_nodes:
                                    env.reset(soft=True)
                                    env.env_state = old_state2.copy()
                                    a_rew2 = a_rew
                                    if n not in list(map(lambda x: x.ip, env.env_state.attacker_obs_state.machines)):
                                        old_state3 = env.env_state.copy()
                                        for a in env_config.attacker_action_conf.actions:
                                            env.reset(soft=True)
                                            env.env_state = old_state3.copy()
                                            a.ip = env.env_state.attacker_obs_state.get_action_ip(a)
                                            s_prime, reward, done = TransitionOperator.attacker_transition(s=env.env_state, attacker_action=a,
                                                                                                           env_config=env_config)
                                            if n in list(map(lambda x: x.ip, s_prime.attacker_obs_state.machines)):
                                                a_rew2 = a_rew2 + reward
                                                env.env_state = s_prime
                                                r_path = k_path + [a]
                                                r_nodes = remaining_nodes.copy()
                                                r_nodes.remove(n)
                                                next_node = n
                                                paths = paths + FindPiStarAttacker._breach_node(path=r_path, current_node=next_node,
                                                                                                remaining_nodes=r_nodes,
                                                                                                rew=a_rew2, env=env,
                                                                                                env_config=env_config,
                                                                                                pivot_actions=pivot_actions)
                                    else:
                                        r_nodes = remaining_nodes.copy()
                                        r_nodes.remove(n)
                                        next_node = n
                                        paths = paths + FindPiStarAttacker._breach_node(path=k_path, current_node=next_node,
                                                                                        remaining_nodes=r_nodes,
                                                                                        rew=a_rew2, env=env, env_config=env_config,
                                                                                        pivot_actions=pivot_actions)
        else:
            a_rew = rew
            for a in pivot_actions:
                a.ip = env.env_state.attacker_obs_state.get_action_ip(a)
                s_prime, reward, done = TransitionOperator.attacker_transition(s=env.env_state, attacker_action=a,
                                                                               env_config=env_config)
                a_rew = reward + a_rew
                path = path + [a]
                env.env_state = s_prime
                if done:
                    paths.append((path, a_rew))
            old_state = env.env_state.copy()
            if not len(remaining_nodes) == 0 and not done:
                # next_node = remaining_nodes[0]
                for n in remaining_nodes:
                    env.reset(soft=True)
                    env.env_state = old_state.copy()
                    a_rew2 = a_rew
                    if n not in list(map(lambda x: x.ip, env.env_state.attacker_obs_state.machines)):
                        old_state2 = env.env_state.copy()
                        for a in env_config.attacker_action_conf.actions:
                            env.reset(soft=True)
                            env.env_state = old_state2.copy()
                            a.ip = env.env_state.attacker_obs_state.get_action_ip(a)
                            s_prime, reward, done = TransitionOperator.attacker_transition(s=env.env_state, attacker_action=a,
                                                                                           env_config=env_config)
                            if n in list(map(lambda x: x.ip, s_prime.attacker_obs_state.machines)):
                                a_rew2 = a_rew2 + reward
                                env.env_state = s_prime
                                r_path = path + [a]
                                r_nodes = remaining_nodes.copy()
                                r_nodes.remove(n)
                                next_node = n
                                paths = paths + FindPiStarAttacker._breach_node(path=r_path, current_node=next_node,
                                                                                remaining_nodes=r_nodes,
                                                                                rew=a_rew2, env=env,
                                                                                env_config=env_config,
                                                                                pivot_actions=pivot_actions)
                    else:
                        r_nodes = remaining_nodes.copy()
                        r_nodes.remove(n)
                        next_node = n
                        paths = paths + FindPiStarAttacker._breach_node(path=path, current_node=next_node,
                                                                        remaining_nodes=r_nodes,
                                                                        rew=a_rew2, env=env, env_config=env_config,
                                                                        pivot_actions=pivot_actions)
        return paths

    @staticmethod
    def pivot_actions(env_config):
        """
        Helper function that returns the actions that are used for pivoting

        :param env_config: the envrironment configuration
        :return: list of action ids for pivoting
        """
        pivot_actions = []

        for a in env_config.attacker_action_conf.actions:
            if a.id == AttackerActionId.NETWORK_SERVICE_LOGIN:
                pivot_actions.append(a)

        for a in env_config.attacker_action_conf.actions:
            if a.id == AttackerActionId.FIND_FLAG:
                pivot_actions.append(a)

        for a in env_config.attacker_action_conf.actions:
            if a.id == AttackerActionId.INSTALL_TOOLS:
                pivot_actions.append(a)

        for a in env_config.attacker_action_conf.actions:
            if a.id == AttackerActionId.SSH_BACKDOOR:
                pivot_actions.append(a)
        return pivot_actions


    @staticmethod
    def upper_bound_pi(env_config) -> float:
        """
        Returns an upper bound reward for an environment

        :param env_config: the environment configuration
        :return: the upper bound reward
        """
        num_flags = len(env_config.network_conf.flags_lookup)
        reward = env_config.attacker_flag_found_reward_mult*num_flags
        reward = reward + env_config.attacker_all_flags_reward
        return reward


    @staticmethod
    def update_pi_star(env_config: PyCREnvConfig, env: "PyCRCTFEnv") -> PyCREnvConfig:
        """
        Update information about the attacker's optimal policy

        :param env_config: the environment configuration
        :param env: the environment
        :return: the updated environment configuration
        """
        if (env_config.env_mode == EnvMode.SIMULATION
            or env_config.env_mode == EnvMode.GENERATED_SIMULATION) \
                and env_config.compute_pi_star_attacker:

            if not env_config.use_upper_bound_pi_star_attacker:
                pi_star_tau_attacker, pi_star_rew_attacker = FindPiStarAttacker.brute_force(env_config, env)
                env_config.pi_star_tau_attacker = pi_star_tau_attacker
                env_config.pi_star_rew_attacker = pi_star_rew_attacker
                env_config.pi_star_rew_list_attacker.append(pi_star_rew_attacker)

        if env_config.use_upper_bound_pi_star_attacker:
            env_config.pi_star_rew_attacker = FindPiStarAttacker.upper_bound_pi(env_config)
            env_config.pi_star_tau_attacker = None
            env_config.pi_star_rew_list_attacker.append(env_config.pi_star_rew_attacker)

        return env_config
