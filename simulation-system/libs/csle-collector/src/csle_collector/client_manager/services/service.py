from typing import List


class Service:
    """
    A service of the network.
    The service might be distributed across several network nodes.
    The service is defined by the series of commands that a client executes to make use of the service.
    """
    def __init__(self, commands: List[str]) -> None:
        """
        Initializes the object

        :param commands: the list of commands
        """
        self.commands = commands