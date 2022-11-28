from typing import List, Dict, Any
from csle_common.dao.simulation_config.player_config import PlayerConfig


class PlayersConfig:
    """
    A DTO representing the configuration of players in a simulation environment
    """

    def __init__(self, player_configs: List[PlayerConfig]):
        """
        Initializes the DTO

        :param player_configs: the list of configurations for each player
        """
        self.player_configs = player_configs

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["player_configs"] = list(map(lambda x: x.to_dict(), self.player_configs))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PlayersConfig":
        """
        Converts a dict representation of the object to a DTO

        :param d: the dict to convert
        :return: the created object
        """
        obj = PlayersConfig(
            player_configs=list(map(lambda x: PlayerConfig.from_dict(x), d["player_configs"]))
        )
        return obj

    def __str__(self):
        """
        :return: a string representation of the DTO
        """
        return f"players_configs: {list(map(lambda x: str(x), self.player_configs))}"
