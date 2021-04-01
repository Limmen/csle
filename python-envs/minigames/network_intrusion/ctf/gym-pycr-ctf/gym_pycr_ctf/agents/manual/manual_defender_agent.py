"""
Manual defender agent
"""
try:
    from gym_pycr_ctf.rendering import Viewer
except:
    pass
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.envs import PyCRCTFEnv
import numpy as np

class ManualDefenderAgent:
    """
    Class representing a manual defender agent, controlled in the GUI by keyboard
    """

    def __init__(self, env_config: EnvConfig, env: PyCRCTFEnv, render: bool = False,
                 attacker_opponent = None):
        """
        Sets up manual defender environment

        :param idsgame_config: the configuration
        """
        self.env = env
        self.env_config = env_config
        self.attacker_opponent = attacker_opponent

        self.env.env_config.defender_action_conf.print_actions()
        if render:
            raise NotImplemented("GUI not implemented for defender currently")
        else:
            num_actions = env.env_config.defender_action_conf.num_actions
            actions = np.array(list(range(num_actions)))
            history = []
            while True:
                raw_input = input(">")
                raw_input = raw_input.strip()
                legal_actions = list(
                    filter(lambda x: env.is_defense_action_legal(x, env.env_config, env.env_state), actions))
                if raw_input == "help":
                    print("Enter an action id to execute the action, "
                          "press R to reset, press S to print the state, press A to print the actions, "
                          "press L to print the legal actions, press x to select a random legal action,"
                          "press H to print the history of actions")
                elif raw_input == "R":
                    env.reset()
                elif raw_input == "S":
                    print(str(env.env_state.defender_obs_state))
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
                else:
                    actions_str = raw_input.split(",")
                    digits_only = any(any(char.isdigit() for char in x) for x in actions_str)
                    attacker_action = None
                    if attacker_opponent is not None:
                        attacker_action = attacker_opponent.action(env.env_state)
                    if not digits_only:
                        print("Invalid action. Actions must be integers.")
                    else:
                        actions = list(map(lambda x: int(x), actions_str))
                        for a in actions:
                            if env.is_defense_action_legal(a, env.env_config, env.env_state):
                                action = (attacker_action, a)
                                print("Attacker action: {}".format(attacker_action))
                                _, _, done, _ = self.env.step(action)
                                history.append(a)
                                if done:
                                    print("done:{}, attacker_caught:{}, stopped:{}".format(
                                        done, env.env_state.defender_obs_state.caught_attacker,
                                        env.env_state.defender_obs_state.stopped
                                    ))
                            else:
                                print("action:{} is illegal".format(a))
