"""
Constants for gym-csle-stopping-game
"""


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
    INTRUSION_LENGTH = "intrusion_length"
    INTRUSION_START = "intrusion_start"
    WEIGHTED_INTRUSION_PREDICTION_DISTANCE = "weighted_intrusion_prediction_distance"
    START_POINT_CORRECT = "start_point_correct"
    INTRUSION_END = "intrusion_end"
    RETURN = "R"
    TIME_HORIZON = "T"
    STOP = "stop"
    STOPS_REMAINING = "l"
    STATE = "s"
    DEFENDER_ACTION = "a1"
    ATTACKER_ACTION = "a2"
    OBSERVATION = "o"
    TIME_STEP = "t"
    AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN = "average_defender_baseline_stop_on_first_alert_return"
    AVERAGE_UPPER_BOUND_RETURN = "average_upper_bound_return"
