from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig


class StoppingGameAttackerMdpConfig:
    """
    DTO class representing the configuration of the MDP environnment of the attacker
    when facing a static defender policy
    """

    def __init__(self, stopping_game_config: StoppingGameConfig, defender_strategy,
                 stopping_game_name: str = "csle-stopping-game-v1"):
        self.stopping_game_config = stopping_game_config
        self.defender_strategy = defender_strategy
        self.stopping_game_name = stopping_game_name