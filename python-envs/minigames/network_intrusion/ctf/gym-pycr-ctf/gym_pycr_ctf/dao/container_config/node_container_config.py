
class NodeContainerConfig:
    """
    A DTO object representing an individual container in an emulation environment
    """

    def __init__(self, name: str, network: str, version: str, level: str, ip: str, minigame: str):
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