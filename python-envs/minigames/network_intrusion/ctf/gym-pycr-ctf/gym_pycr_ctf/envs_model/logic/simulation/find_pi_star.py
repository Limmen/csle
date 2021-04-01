from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.envs_model.logic.transition_operator import TransitionOperator
from gym_pycr_ctf.dao.action.attacker.attacker_action_id import AttackerActionId

class FindPiStar:

    @staticmethod
    def brute_force(env_config: EnvConfig, env):
        print("brute")
        shortest_paths = env_config.network_conf.shortest_paths()
        if len(shortest_paths) == 0:
            return [], -1
        p = shortest_paths[0]
        paths = []
        pivot_actions = FindPiStar.pivot_actions(env_config=env_config)
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
                    paths = paths + FindPiStar._breach_node(path=[a], current_node=next_node, remaining_nodes=r_nodes,
                                                            rew=reward, env=env, env_config=env_config,
                                                            pivot_actions=pivot_actions)
                    env.reset(soft=True)
        sorted_paths = sorted(paths, key=lambda x: x[1])
        pi_star =sorted_paths[-1]
        return pi_star[0], pi_star[1]

    @staticmethod
    def _breach_node(path, current_node, remaining_nodes, rew, env, env_config, pivot_actions):
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
                                                paths = paths + FindPiStar._breach_node(path=r_path, current_node=next_node,
                                                                                        remaining_nodes=r_nodes,
                                                                                        rew=a_rew2, env=env,
                                                                                        env_config=env_config,
                                                                                        pivot_actions=pivot_actions)
                                    else:
                                        r_nodes = remaining_nodes.copy()
                                        r_nodes.remove(n)
                                        next_node = n
                                        paths = paths + FindPiStar._breach_node(path=k_path, current_node=next_node,
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
                                paths = paths + FindPiStar._breach_node(path=r_path, current_node=next_node,
                                                                        remaining_nodes=r_nodes,
                                                                        rew=a_rew2, env=env,
                                                                        env_config=env_config,
                                                                        pivot_actions=pivot_actions)
                    else:
                        r_nodes = remaining_nodes.copy()
                        r_nodes.remove(n)
                        next_node = n
                        paths = paths + FindPiStar._breach_node(path=path, current_node=next_node,
                                                                remaining_nodes=r_nodes,
                                                                rew=a_rew2, env=env, env_config=env_config,
                                                                pivot_actions=pivot_actions)
        return paths

    @staticmethod
    def pivot_actions(env_config):
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
    def upper_bound_pi(env_config):
        #shortest_path = env_config.network_conf.shortest_paths()[0][0]
        num_flags = len(env_config.network_conf.flags_lookup)
        reward = env_config.flag_found_reward_mult*num_flags
        reward = reward + env_config.all_flags_reward
        return reward

