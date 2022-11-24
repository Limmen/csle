from csle_common.dao.domain_randomization.randomization_space_config import RandomizationSpaceConfig


class RandomizationSpace:
    """
    Object representing a randomization space
    """

    def __init__(self, config: RandomizationSpaceConfig):
        """
        Initializes the randomization space

        :param config: the randomization space config
        """
        self.config = config

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"config:{str(self.config)}"
