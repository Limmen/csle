"""
Manual defender agent
"""
try:
    from gym_pycr_ctf.rendering.viewer import Viewer
except:
    pass
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.envs import PyCRCTFEnv
import numpy as np
import torch


class ManualDefenderAgent:
    """
    Class representing a manual defender agent, controlled in the GUI by keyboard
    """

    def __init__(self, env_config: EnvConfig, env: PyCRCTFEnv, render: bool = False, model = None):
        """
        Sets up manual defender environment

        :param idsgame_config: the configuration
        """
        self.env = env
        self.env_config = env_config
        self.model = model

        self.env.env_config.defender_action_conf.print_actions()
        if render:
            raise NotImplemented("GUI not implemented for defender currently")
        else:
            num_actions = env.env_config.defender_action_conf.num_actions
            actions = np.array(list(range(num_actions)))
            history = []
            latest_obs = None
            latest_rew = None
            latest_obs = env.reset()
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
                    latest_obs = env.reset()
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
                elif raw_input == "O":
                    print(latest_obs[1].tolist())
                elif raw_input == "U":
                    print(latest_rew)
                else:
                    actions_str = raw_input.split(",")
                    digits_only = any(any(char.isdigit() for char in x) for x in actions_str)
                    attacker_action = None
                    if not digits_only:
                        print("Invalid action. Actions must be integers.")
                    else:
                        actions = list(map(lambda x: int(x), actions_str))
                        for a in actions:
                            if env.is_defense_action_legal(a, env.env_config, env.env_state):
                                action = (attacker_action, a)
                                print("Attacker action: {}".format(attacker_action))
                                latest_obs, latest_rew, done, _ = self.env.step(action)
                                if self.model is not None:
                                    attacker_obs, defender_obs = latest_obs
                                    obs_tensor = torch.as_tensor(defender_obs.flatten()).to(self.device)
                                    actions, values = self.model.predict(observation=obs_tensor, deterministic=True,
                                                                         state=obs_tensor, attacker=False,
                                                                         infos={},
                                                                         env_config=self.env.env_config,
                                                                         env_configs=None, env=self.env,
                                                                         env_idx=0,
                                                                         env_state=self.env.env_state
                                                                         )
                                history.append(a)
                                if done:
                                    print("done:{}, attacker_caught:{}, stopped:{}, intrusion_completed:{}".format(
                                        done, env.env_state.defender_obs_state.caught_attacker,
                                        env.env_state.defender_obs_state.stopped,
                                        env.env_state.attacker_obs_state.intrusion_completed
                                    ))
                            else:
                                print("action:{} is illegal".format(a))
