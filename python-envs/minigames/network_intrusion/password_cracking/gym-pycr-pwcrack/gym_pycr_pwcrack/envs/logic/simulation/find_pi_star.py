from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.envs.logic.transition_operator import TransitionOperator

class FindPiStar:

    @staticmethod
    def brute_force(env_config: EnvConfig, env):
        shortest_paths = env_config.network_conf.shortest_paths()
        p = shortest_paths[0]
        paths = []
        env.reset()
        for n in p:
            for a in env_config.action_conf.actions:
                s_prime, reward, done = TransitionOperator.transition(s=env.env_state, a=a, env_config=env_config)
                if n in list(map(lambda x: x.ip, s_prime.obs_state.machines)):
                    env.env_state = s_prime
                    paths = paths + FindPiStar._find_node(path=[a], current_node=n, remaining_nodes=p[1:], rew=reward)
                    env.reset()


    @staticmethod
    def _find_node(path, current_node, remaining_nodes, rew, env, env_config):
        for n in remaining_nodes:
            for a in env_config.action_conf.actions:
                s_prime, reward, done = TransitionOperator.transition(s=env.env_state, a=a, env_config=env_config)
                if n in list(map(lambda x: x.ip, s_prime.obs_state.machines)):
                    env.env_state = s_prime
                    paths = paths + FindPiStar._find_node(path=[a], current_node=n, remaining_nodes=p[1:], rew=reward)
                    env.reset()

    @staticmethod
    def _breach_node(path, current_node, remaining_nodes, rew, env, env_config):
        for n in remaining_nodes:
            for a in env_config.action_conf.actions:
                s_prime, reward, done = TransitionOperator.transition(s=env.env_state, a=a, env_config=env_config)
                for k in s_prime.obs_state.machines:
                    if k.ip == current_node:
                        if k.shell_access:
                            env.env_state = s_prime
                            # TODO hard code scan/find flag
                            if len(remaining_nodes) == 0:
                                pass # TODO
                            else:
                                next_node = remaining_nodes[0]
                                path = path + a
                                rew = reward + rew
                                if n not in list(map(lambda x: x.ip, s_prime.obs_state.machines)):
                                    paths = paths + FindPiStar._find_node(path=path, current_node=next_node,
                                                                          remaining_nodes=remaining_nodes[1:],
                                                                          rew=reward)
                                else:
                                    paths = paths + FindPiStar._breach_node(path=path, current_node=next_node,
                                                                          remaining_nodes=remaining_nodes[1:],
                                                                          rew=reward)
                            env.reset()
                    env.reset()
