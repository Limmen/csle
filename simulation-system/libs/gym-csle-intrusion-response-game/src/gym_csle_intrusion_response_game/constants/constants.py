"""
Constants for gym-csle-intrusion-response-game
"""
import numpy as np


class ZONES:
    """
    Constants related to the zones of the network
    """
    REDIRECTION_ZONE = 2
    SHUTDOWN_ZONE = 1


class STATES:
    """
    Constants related to the state space of the game
    """
    TERMINAL_STATE = np.array([-1, -1])
    D_STATE_INDEX = 0
    A_STATE_INDEX = 1


class ATTACK_STATES:
    """
    Constants related to the attack state semantics
    """
    HEALTHY = 0
    RECON = 1
    COMPROMISED = 2


class ATTACKER_ACTIONS:
    """
    Constants related to the local attacker actions
    """
    WAIT = 0
    RECON = 1
    BRUTE_FORCE = 2
    EXPLOIT = 3


class DEFENDER_ACTIONS:
    """
    Constants related to the local defender actions
    """
    WAIT = 0


class STATIC_DEFENDER_STRATEGIES:
    """
    String constants representing static defender strategies
    """
    RANDOM = "random"


class STATIC_ATTACKER_STRATEGIES:
    """
    String constants representing static attacker strategies
    """
    RANDOM = "random"


class ENV_METRICS:
    """
    String constants representing environment metrics
    """
    RETURN = "R"
    TIME_HORIZON = "T"
    STATE = "s"
    DEFENDER_ACTION = "a1"
    ATTACKER_ACTION = "a2"
    OBSERVATION = "o"
    TIME_STEP = "t"
    AVERAGE_UPPER_BOUND_RETURN = "average_upper_bound_return"
    AVERAGE_RANDOM_RETURN = "average_random_return"
