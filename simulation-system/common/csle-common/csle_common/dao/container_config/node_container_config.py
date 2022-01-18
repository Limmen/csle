
class NodeContainerConfig:
    """
    A DTO object representing an individual container in an emulation environment
    """

    def __init__(self, name: str, internal_network: str, external_network: str,
                 version: str, level: str, internal_ip: str,
                 external_ip : str,
                 minigame: str, restart_policy: str, connected_to_external_net : bool,
                 connected_to_internal_net : bool, suffix: str):
        """
        Intializes the DTO

        :param name: the name of the node container
        :param internal_network: the internal network name
        :param external_network: the external network name
        :param version: the version of the container
        :param level: the level of the container
        :param internal_ip: the internal ip
        :param external_ip: the external ip
        :param minigame: the minigame that it belongs to
        :param restart_policy: the restart policy of the container
        :param connected_to_external_net: a boolean flag that indicates whether the container is connected
                                          to the external network or not
        :param connected_to_internal_net: a boolean flag that indicates whether the container is connected
                                                  to the internal network or not
        :param suffix: the suffix of the container id
        """
        self.name = name
        self.internal_network = internal_network
        self.version = version
        self.level = level
        self.internal_ip = internal_ip
        self.minigame = minigame
        self.restart_policy = restart_policy
        self.external_network = external_network
        self.external_ip = external_ip
        self.connected_to_external_net = connected_to_external_net
        self.connected_to_internal_net = connected_to_internal_net
        self.suffix = suffix

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "name:{}, internal_network:{}, version:{}, internal_fip:{}, minigame:{}, restart_policy:{}, " \
               "external_network:{}, external_ip:{}, connected_to_internal_net:{}, " \
               "connected_to_external_net:{}, suffix:{}".format(
            self.name,self.internal_network, self.version, self.level, self.internal_ip, self.minigame,
            self.restart_policy,
            self.external_network, self.external_ip, self.connected_to_internal_net, self.connected_to_external_net,
            self.suffix)