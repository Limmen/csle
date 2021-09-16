"""
Manual attacker agent
"""
try:
    from pycr_common.rendering.viewer import Viewer
except:
    pass
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.envs import PyCRCTFEnv
from pycr_common.dao.agent.agent_type import AgentType
import numpy as np


class ManualAttackerAgent:
    """
    Class representing a manual attacker agent, controlled in the GUI by keyboard
    """

    def __init__(self, env_config: EnvConfig, env: PyCRCTFEnv, render: bool = False,
                 defender_opponent: AgentType = None):
        """
        Sets up the GUI with the manual attacker

        :param idsgame_config: the configuration
        """
        self.env = env
        self.env_config = env_config
        self.defender_opponent = defender_opponent

        self.env.env_config.attacker_action_conf.print_actions()
        if render:
            agent_state = self.env.attacker_agent_state
            viewer = Viewer(self.env_config, init_state=agent_state)
            viewer.manual_start_attacker(env=self.env)
        else:
            num_actions = env.env_config.attacker_action_conf.num_actions
            actions = np.array(list(range(num_actions)))
            cumulative_reward = 0
            latest_obs = None
            latest_rew = None
            latest_obs = env.reset()
            history = []
            while True:
                raw_input = input(">")
                raw_input = raw_input.strip()
                legal_actions = list(
                    filter(lambda x: env.is_attack_action_legal(x, env.env_config, env.env_state), actions))
                if raw_input == "help":
                    print("Enter an action id to execute the action, "
                          "press R to reset, press S to print the state, press A to print the actions, "
                          "press L to print the legal actions, press x to select a random legal action,"
                          "press H to print the history of actions")
                elif raw_input == "R":
                    latest_obs = env.reset()
                    cumulative_reward = 0
                elif raw_input == "S":
                    print(str(env.env_state.attacker_obs_state))
                elif raw_input == "L":
                    print(legal_actions)
                elif raw_input == "x":
                    a = np.random.choice(legal_actions)
                    _, _, done, _ = self.env.step(a)
                    history.append(a)
                    if done:
                        print("done:{}".format(done))
                elif raw_input == "H":
                    print(history)
                elif raw_input == "O":
                    print(latest_obs)
                    print(latest_obs[0].shape)
                    print(latest_obs[1].shape)
                elif raw_input == "U":
                    print(latest_rew)
                elif raw_input == "P":
                    print(cumulative_reward)
                else:
                    actions_str = raw_input.split(",")
                    digits_only = any(any(char.isdigit() for char in x) for x in actions_str)
                    defender_action = None
                    if defender_opponent is not None:
                        defender_action = defender_opponent.action(env.env_state)
                    if not digits_only:
                        print("Invalid action. Actions must be integers.")
                    else:
                        actions = list(map(lambda x: int(x), actions_str))
                        for a in actions:
                            if env.is_attack_action_legal(a, env.env_config, env.env_state):
                                action = (a, defender_action)
                                latest_obs, latest_rew, done, _ = self.env.step(action)
                                attacker_rew, defender_rew = latest_rew
                                cumulative_reward += attacker_rew
                                history.append(a)
                                if done:
                                    print("done:{}, attacker_caught:{}, stopped:{}, all_flags:{}, rew:{}".format(
                                        done, env.env_state.defender_obs_state.caught_attacker,
                                        env.env_state.defender_obs_state.stopped,
                                        env.env_state.attacker_obs_state.all_flags,
                                        latest_rew
                                    ))
                            else:
                                print("action:{} is illegal".format(a))
