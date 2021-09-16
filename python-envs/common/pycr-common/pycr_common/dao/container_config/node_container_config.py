
class NodeContainerConfig:
    """
    A DTO object representing an individual container in an emulation environment
    """

    def __init__(self, name: str, network: str, version: str, level: str, ip: str, minigame: str):
        """
        Intializes the DTO

        :param name: the name of the node container
        :param network: the network name
        :param version: the version of the container
        :param level: the level of the container
        :param ip: the ip
        :param minigame: the minigame that it belongs to
        """
        self.name = name
        self.network = network
        self.version = version
        self.level = level
        self.ip = ip
        self.minigame = minigame


    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "name:{}, network:{}, version:{}, ip:{}, minigame:{}".format(
            self.name,self.network, self.version, self.level, self.ip, self.minigame)