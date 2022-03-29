from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig


class StoppingGameDefenderPomdpConfig:
    """
    DTO class representing the configuration of the POMDP environnment of the defender
    when facing a static attacker policy
    """

    def __init__(self, stopping_game_config: StoppingGameConfig, attacker_strategy,
                 stopping_game_name: str = "csle-stopping-game-v1"):
        self.stopping_game_config = stopping_game_config
        self.attacker_strategy = attacker_strategy
        self.stopping_game_name = stopping_game_name