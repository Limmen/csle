from typing import List
import numpy as np
from scipy.stats import betabinom
from csle_common.dao.network.emulation_env_agent_config import EmulationEnvAgentConfig
from csle_common.dao.network.emulation_env_state import EmulationEnvState
from csle_common.dao.action.attacker.attacker_action_id import AttackerActionId
from csle_common.envs_model.util.env_dynamics_util import EnvDynamicsUtil
from csle_common.dao.action.attacker.attacker_action_type import AttackerActionType
from csle_common.dao.action.attacker.attacker_action_outcome import AttackerActionOutcome
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig


class EnvUtil:
    """
    Class with utility functions for the StoppingGame Environment
    """

    @staticmethod
    def b0() -> np.ndarray:
        """
        :return: the initial belief
        """
        return np.array([1, 0, 0])

    @staticmethod
    def state_space():
        return np.array([0, 1, 2])

    @staticmethod
    def defender_actions() -> np.ndarray:
        """
        :return: the action space of the defender
        """
        return np.array([0, 1])

    @staticmethod
    def attacker_actions() -> np.ndarray:
        """
        :return: the action space of the attacker
        """
        return np.array([0, 1])

    @staticmethod
    def observation_space(n):
        """
        Returns the observation space of size n

        :param n: the size of the observation space
        :return: O
        """
        return np.array(list(range(n)))

    @staticmethod
    def reward_tensor(l: int, R_SLA: int, R_INT: int, R_COST: int, L: int, R_ST: int) -> np.ndarray:
        """
        :param l: the number of stops remaining
        :param R_SLA: the R_SLA constant
        :param R_INT: the R_INT constant
        :param R_COST: the R_COST constant
        :param R_ST: the R_ST constant
        :return: a |A1|x|A2|x|S| tensor
        """
        R = np.array(
            [
                # Defender continues
                [
                    # Attacker continues
                    [R_SLA, R_SLA + R_INT, 0],
                    # Attacker stops
                    [R_SLA, R_SLA, 0]
                ],
                # Defender stops
                [
                    # Attacker continues
                    [R_COST / L, R_ST / l, 0],
                    # Attacker stops
                    [R_COST / L, R_SLA, 0]
                ]
            ]
        )
        return R

    @staticmethod
    def transition_tensor(l: int, p: float) -> np.ndarray:
        """
        :param l: the number of stops remaining
        :return: a |A1|x|A2||S|^2 tensor
        """
        if l == 1:
            return np.array(
                [
                    # Defender continues
                    [
                        # Attacker continues
                        [
                            [1 - p, 0, p],  # No intrusion
                            [0, 1 - p, p],  # Intrusion
                            [0, 0, 1]  # Terminal
                        ],
                        # Attacker stops
                        [
                            [0, 1 - p, p],  # No intrusion
                            [0, 0, 1],  # Intrusion
                            [0, 0, 1]  # Terminal
                        ]
                    ],

                    # Defender stops
                    [
                        # Attacker continues
                        [
                            [0, 0, 1],  # No intrusion
                            [0, 0, 1],  # Intrusion
                            [0, 0, 1]  # Terminal
                        ],
                        # Attacker stops
                        [
                            [0, 0, 1],  # No Intrusion
                            [0, 0, 1],  # Intrusion
                            [0, 0, 1]  # Terminal
                        ]
                    ]
                ]
            )
        else:
            return np.array(
                [
                    # Defender continues
                    [
                        # Attacker continues
                        [
                            [1 - p, 0, p],  # No intrusion
                            [0, 1 - p, p],  # Intrusion
                            [0, 0, 1]  # Terminal
                        ],
                        # Attacker stops
                        [
                            [0, 1 - p, p],  # No intrusion
                            [0, 0, 1],  # Intrusion
                            [0, 0, 1]  # Terminal
                        ]
                    ],

                    # Defender stops
                    [
                        # Attacker continues
                        [
                            [1 - p, 0, p],  # No intrusion
                            [0, 1 - p, p],  # Intrusion
                            [0, 0, 1]  # Terminal
                        ],
                        # Attacker stops
                        [
                            [0, 1 - p, p],  # No Intrusion
                            [0, 0, 1],  # Intrusion
                            [0, 0, 1]  # Terminal
                        ]
                    ]
                ]
            )

    @staticmethod
    def observation_tensor(n):
        """
        :return: a |S|x|O| tensor
        """
        intrusion_dist = []
        no_intrusion_dist = []
        terminal_dist = np.zeros(n)
        terminal_dist[-1] = 1
        intrusion_rv = betabinom(n=n, a=1, b=0.9)
        no_intrusion_rv = betabinom(n=n, a=0.7, b=2)
        for i in range(n):
            intrusion_dist.append(intrusion_rv.pmf(i))
            no_intrusion_dist.append(no_intrusion_rv.pmf(i))
        Z = np.array(
            [
                [
                    [
                        no_intrusion_dist,
                        intrusion_dist,
                        terminal_dist
                    ],
                    [
                        no_intrusion_dist,
                        intrusion_dist,
                        terminal_dist
                    ],
                ],
                [
                    [
                        no_intrusion_dist,
                        intrusion_dist,
                        terminal_dist
                    ],
                    [
                        no_intrusion_dist,
                        intrusion_dist,
                        terminal_dist
                    ],
                ]
            ]
        )
        return Z


    @staticmethod
    def is_defense_action_legal(defense_action_id: int, env_config: EmulationEnvAgentConfig, env_state: EmulationEnvState) -> bool:
        """
        Checks if a given defense action is legal in the current state of the environment

        :param defense_action_id: the id of the action to check
        :param env_config: the environment config
        :param env_state: the environment state
        :param attacker_action: the id of the previous attack action
        :return: True if legal, else false
        """
        return True

    @staticmethod
    def is_attack_action_legal(attack_action_id: int, env_config: EmulationEnvAgentConfig, env_state: EmulationEnvState) -> bool:
        """
        Checks if a given attack action is legal in the current state of the environment

        :param attack_action_id: the id of the action to check
        :param env_config: the environment config
        :param env_state: the environment state
        :return: True if legal, else false
        """
        if attack_action_id > len(env_config.attacker_action_conf.actions) - 1:
            return False

        action = env_config.attacker_action_conf.actions[attack_action_id]
        ip = env_state.attacker_obs_state.get_action_ips(action)

        logged_in_ips_str = EnvDynamicsUtil.logged_in_ips_str(emulation_env_config=env_config, a=action, s=env_state,
                                                              full_ip_str=True)
        if (action.id, action.index, logged_in_ips_str) in env_state.attacker_obs_state.actions_tried:
            return False

        # Recon on subnet is always possible
        if action.type == AttackerActionType.RECON and action.subnet:
            return True

        # Recon on set of all found machines is always possible if there exists such machiens
        if action.type == AttackerActionType.RECON and action.index == -1 and len(
                env_state.attacker_obs_state.machines) > 0:
            return True

        # Optimal Stopping actions are always possible
        if action.type == AttackerActionType.STOP or action.type == AttackerActionType.CONTINUE:
            return True

        machine_discovered = False
        target_machine = None
        target_machines = []
        logged_in = False
        unscanned_filesystems = False
        untried_credentials = False
        root_login = False
        machine_root_login = False
        machine_logged_in = False
        uninstalled_tools = False
        machine_w_tools = False
        uninstalled_backdoor = False
        target_untried_credentials = False

        for m in env_state.attacker_obs_state.machines:
            if m.logged_in:
                logged_in = True
                if not m.filesystem_searched:
                    unscanned_filesystems = True
                if m.root:
                    root_login = True
                    if not m.tools_installed and not m.install_tools_tried:
                        uninstalled_tools = True
                    else:
                        machine_w_tools = True
                    if m.tools_installed and not m.backdoor_installed and not m.backdoor_tried:
                        uninstalled_backdoor = True
            if m.ips == ip:
                machine_discovered = True
                target_machine = m
                if m.logged_in:
                    machine_logged_in = True
                    if m.root:
                        machine_root_login = True
                if m.untried_credentials:
                    target_untried_credentials = m.untried_credentials
            # if m.shell_access and not m.logged_in:
            #     untried_credentials = True
            if m.untried_credentials:
                untried_credentials = m.untried_credentials

        if action.subnet or action.id == AttackerActionId.NETWORK_SERVICE_LOGIN:
            machine_discovered = True

        # Privilege escalation only legal if machine discovered and logged in and not root
        if action.type == AttackerActionType.PRIVILEGE_ESCALATION and (not machine_discovered or not machine_logged_in
                                                                       or machine_root_login):
            return False

        # Exploit only legal if we have not already compromised the node
        if action.type == AttackerActionType.EXPLOIT and machine_logged_in and root_login:
            return False

        # Shell-access Exploit only legal if we do not already have untried credentials
        if action.type == AttackerActionType.EXPLOIT and action.action_outcome == AttackerActionOutcome.SHELL_ACCESS \
                and target_untried_credentials:
            return False

        # Priv-Esc Exploit only legal if we are already logged in and do not have root
        if action.type == AttackerActionType.EXPLOIT \
                and action.action_outcome == AttackerActionOutcome.PRIVILEGE_ESCALATION_ROOT \
                and (not machine_logged_in or root_login):
            return False

        # If IP is discovered, then IP specific action without other prerequisites is legal
        if machine_discovered and (action.type == AttackerActionType.RECON or action.type == AttackerActionType.EXPLOIT
                                   or action.type == AttackerActionType.PRIVILEGE_ESCALATION):
            if action.subnet and target_machine is None:
                return True
            else:
                exploit_tried = env_state.attacker_obs_state.exploit_tried(a=action, m=target_machine)
            if exploit_tried:
                return False
            return True

        # If nothing new to scan, find-flag is illegal
        if action.id == AttackerActionId.FIND_FLAG and not unscanned_filesystems:
            return False

        # If nothing new to backdoor, install backdoor is illegal
        if action.id == AttackerActionId.SSH_BACKDOOR and not uninstalled_backdoor:
            return False

        # If no new credentials, login to service is illegal
        if action.id == AttackerActionId.NETWORK_SERVICE_LOGIN and not untried_credentials:
            return False

        # Pivot recon possible if logged in on pivot machine with tools installed
        if machine_discovered and action.type == AttackerActionType.POST_EXPLOIT and logged_in and machine_w_tools:
            return True

        # If IP is discovered, and credentials are found and shell access, then post-exploit actions are legal
        if machine_discovered and action.type == AttackerActionType.POST_EXPLOIT \
                and ((target_machine is not None and target_machine.shell_access
                      and len(target_machine.shell_access_credentials) > 0)
                     or action.subnet or action.id == AttackerActionId.NETWORK_SERVICE_LOGIN):
            return True

        # Bash action not tied to specific IP only possible when having shell access and being logged in
        if action.id == AttackerActionId.FIND_FLAG and logged_in and unscanned_filesystems:
            return True

        # Bash action not tied to specific IP only possible when having shell access and being logged in and root
        if action.id == AttackerActionId.INSTALL_TOOLS and logged_in and root_login and uninstalled_tools:
            return True

        # Bash action not tied to specific IP only possible when having shell access and being logged in and root
        if action.id == AttackerActionId.SSH_BACKDOOR and logged_in and root_login and machine_w_tools and uninstalled_backdoor:
            return True

        return False

    @staticmethod
    def sample_next_state(T: np.ndarray, s: int, a1: int, a2: int, S: np.ndarray) -> int:
        """
        Samples the next state

        :param T: the transition operator
        :param s: the currrent state
        :param a1: the defender action
        :param a2: the attacker action
        :param S: the state space
        :return: s'
        """
        state_probs = []
        for s_prime in S:
            state_probs.append(T[a1][a2][s][s_prime])
        s_prime = np.random.choice(np.arange(0, len(S)), p=state_probs)
        return s_prime

    @staticmethod
    def sample_initial_state(b1: np.ndarray) -> int:
        """
        Samples the initial state

        :param b1: the initial belief
        :return: s1
        """
        s1 = np.random.choice(np.arange(0, len(b1)), p=b1)
        return s1

    @staticmethod
    def sample_next_observation(Z: np.ndarray, s_prime: int, O: np.ndarray) -> int:
        """
        Samples the next observation

        :param s_prime: the new state
        :param O: the observation space
        :return: o
        """
        observation_probs = []
        for o in O:
            observation_probs.append(Z[0][0][s_prime][o])
        o = np.random.choice(np.arange(0, len(O)), p=observation_probs)
        return o


    @staticmethod
    def bayes_filter(s_prime: int, o: int, a1: int, b: np.ndarray, pi_2: np.ndarray, l: int,
                     config: StoppingGameConfig) -> float:
        """
        A Bayesian filter to compute the belief of player 1
        of being in s_prime when observing o after taking action a in belief b given that the opponent follows
        strategy pi_2

        :param s_prime: the state to compute the belief of
        :param o: the observation
        :param a1: the action of player 1
        :param b: the current belief point
        :param pi_2: the policy of player 2
        :param l: stops remaining
        :return: b_prime(s_prime)
        """
        l=l-1
        norm = 0
        for s in config.S:
            for a2 in config.A2:
                for s_prime_1 in config.S:
                    prob_1 = config.Z[a1][a2][s_prime_1][o]
                    norm += b[s]*prob_1*config.T[l][a1][a2][s][s_prime_1]*pi_2[s][a2]

        if norm == 0:
            return 0
        temp = 0

        for s in config.S:
            for a2 in config.A2:
                temp += config.Z[a1][a2][s_prime][o]*config.T[l][a1][a2][s][s_prime]*b[s]*pi_2[s][a2]

        b_prime_s_prime = temp/norm
        if round(b_prime_s_prime,2) > 1:
            print(f"b_prime_s_prime >= 1: {b_prime_s_prime}, a1:{a1}, s_prime:{s_prime}, l:{l}, o:{o}, pi_2:{pi_2}")
        assert round(b_prime_s_prime,2) <=1
        if s_prime == 2 and o != config.O[-1]:
            assert round(b_prime_s_prime,2) <= 0.01
        return b_prime_s_prime

    @staticmethod
    def p_o_given_b_a1_a2(o: int, b: List, a1: int, a2: int, config: StoppingGameConfig) -> float:
        """
        Computes P[o|a,b]

        :param o: the observation
        :param b: the belief point
        :param a1: the action of player 1
        :param a2: the action of player 2
        :param config: the game config
        :return: the probability of observing o when taking action a in belief point b
        """
        prob = 0
        for s in config.S:
            for s_prime in config.S:
                prob += b[s] * config.T[a1][a2][s][s_prime] * config.Z[a1][a2][s_prime][o]
        assert prob < 1
        return prob

    @staticmethod
    def next_belief(o: int, a1: int, b: np.ndarray, pi_2: np.ndarray, config: StoppingGameConfig, l: int,
                    a2 : int = 0, s : int = 0) -> np.ndarray:
        """
        Computes the next belief using a Bayesian filter

        :param o: the latest observation
        :param a1: the latest action of player 1
        :param b: the current belief
        :param pi_2: the policy of player 2
        :param config: the game config
        :param l: stops remaining
        :param a2: the attacker action (for debugging, should be consistent with pi_2)
        :param s: the true state (for debugging)
        :return: the new belief
        """
        b_prime = np.zeros(len(config.S))
        for s_prime in config.S:
            b_prime[s_prime] = EnvUtil.bayes_filter(s_prime=s_prime, o=o, a1=a1, b=b,
                                                                    pi_2=pi_2, config=config, l=l)
        if round(sum(b_prime), 2) != 1:
            print(f"error, b_prime:{b_prime}, o:{o}, a1:{a1}, b:{b}, pi_2:{pi_2}, "
                  f"a2: {a2}, s:{s}")
        assert round(sum(b_prime), 2) == 1
        return b_prime