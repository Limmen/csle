from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.envs.logic.transition_operator import TransitionOperator
from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action.action_id import ActionId

class FindPiStar:

    @staticmethod
    def brute_force(env_config: EnvConfig, env):
        shortest_paths = env_config.network_conf.shortest_paths()
        p = shortest_paths[0]
        paths = []
        pivot_actions = FindPiStar.pivot_actions(env_config=env_config)
        env.reset()
        p = p[0]
        print("p:{}".format(p))
        for n in p:
            for a in env_config.action_conf.actions:
                s_prime, reward, done = TransitionOperator.transition(s=env.env_state, a=a, env_config=env_config)
                #print("n:{}, list:{}".format(n[0], list(map(lambda x: x.ip, s_prime.obs_state.machines))))
                if n in list(map(lambda x: x.ip, s_prime.obs_state.machines)):
                    # print("node found")
                    env.env_state = s_prime
                    #print("breach node call, n:{}".format(n))
                    print("first action:{}".format(a))
                    paths = paths + FindPiStar._breach_node(path=[a], current_node=n, remaining_nodes=p[1:],
                                                            rew=reward, env=env, env_config=env_config,
                                                            pivot_actions=pivot_actions)
                    env.reset()

        print("paths:{}".format(paths))


    # @staticmethod
    # def _find_node(path, current_node, remaining_nodes, rew, env, env_config, pivot_actions):
    #     paths = []
    #     node_found = False
    #     for n in remaining_nodes:
    #         for a in env_config.action_conf.actions:
    #             s_prime, reward, done = TransitionOperator.transition(s=env.env_state, a=a, env_config=env_config)
    #             if n in list(map(lambda x: x.ip, s_prime.obs_state.machines)):
    #                 env.env_state = s_prime
    #                 node_found = True
    #                 path = path + [a]
    #                 r_nodes = remaining_nodes.copy()
    #                 r_nodes.remove(n)
    #                 print("remaining nodes:{}, current node:{}".format(remaining_nodes, current_node))
    #                 paths = paths + FindPiStar._breach_node(path=path, current_node=n,
    #                                                         remaining_nodes=r_nodes, rew=reward,
    #                                                         env=env, env_config=env_config,
    #                                                         pivot_actions=pivot_actions)
    #                 env.reset()
    #     if not node_found:
    #         raise ValueError("Node not found")
    #     return paths

    @staticmethod
    def _breach_node(path, current_node, remaining_nodes, rew, env, env_config, pivot_actions):
        #print("current node:{}, remaining nodes:{}".format(current_node, remaining_nodes))
        paths = []
        #for n in remaining_nodes:
        for a in env_config.action_conf.actions:
            s_prime, reward, done = TransitionOperator.transition(s=env.env_state, a=a, env_config=env_config)
            for k in s_prime.obs_state.machines:
                #print("current node:{}, ip:{}".format(current_node, k.ip))
                if k.ip == current_node:
                    if k.shell_access:
                        path = path + [a]
                        #print("shell access")
                        env.env_state = s_prime
                        for a in pivot_actions:
                            s_prime, reward, done = TransitionOperator.transition(s=env.env_state, a=a,
                                                                                  env_config=env_config)
                            rew = reward + rew
                            path = path + [a]
                            env.env_state = s_prime
                            if done:
                                print("done:{}".format(done))
                                paths = paths + path

                        if not len(remaining_nodes) == 0 and not done:
                            #next_node = remaining_nodes[0]
                            rew = reward + rew
                            for n in remaining_nodes:
                                if n not in list(map(lambda x: x.ip, s_prime.obs_state.machines)):
                                    for a in env_config.action_conf.actions:
                                        s_prime, reward, done = TransitionOperator.transition(s=env.env_state, a=a,
                                                                                              env_config=env_config)
                                        if n in list(map(lambda x: x.ip, s_prime.obs_state.machines)):
                                            env.env_state = s_prime
                                            r_path = path + [a]
                                            r_nodes = remaining_nodes.copy()
                                            r_nodes.remove(n)
                                            next_node = n
                                            #print("recursion")
                                            paths = paths + FindPiStar._breach_node(path=r_path, current_node=next_node,
                                                                                    remaining_nodes=r_nodes,
                                                                                    rew=reward, env=env,
                                                                                    env_config=env_config,
                                                                                    pivot_actions=pivot_actions)
                                else:
                                    r_nodes = remaining_nodes.copy()
                                    r_nodes.remove(n)
                                    next_node = n
                                    #print("recursion")
                                    paths = paths + FindPiStar._breach_node(path=path, current_node=next_node,
                                                                          remaining_nodes=remaining_nodes[1:],
                                                                          rew=reward, env=env, env_config=env_config,
                                                                          pivot_actions=pivot_actions)
                        else:
                            print("done:{} or no remaining:{}, actions:{}".format(done, remaining_nodes, list(map(lambda x: x.id, path))))
                        env.reset()
                env.reset()
        print("breach returning:{}".format(paths))
        return paths

    @staticmethod
    def pivot_actions(env_config):
        pivot_actions = []

        for a in env_config.action_conf.actions:
            if a.id == ActionId.NETWORK_SERVICE_LOGIN:
                pivot_actions.append(a)

        for a in env_config.action_conf.actions:
            if a.id == ActionId.FIND_FLAG:
                pivot_actions.append(a)

        for a in env_config.action_conf.actions:
            if a.id == ActionId.INSTALL_TOOLS:
                pivot_actions.append(a)

        for a in env_config.action_conf.actions:
            if a.id == ActionId.SSH_BACKDOOR:
                pivot_actions.append(a)
        return pivot_actions
