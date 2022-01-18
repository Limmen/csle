
class ContainerNetwork:
    """
    DTO representing an IP network of virtual containers
    """

    def __init__(self, name: str, subnet_mask: str, subnet_prefix: str):
        """
        Initializes the DTO

        :param name: the name of the network
        :param subnet_mask: the subnet mask of the network
        """
        self.name = name
        self.subnet_mask = subnet_mask
        self.subnet_prefix = subnet_prefix


    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"name:{self.name}, subnet_mask:{self.subnet_mask}, subnet_prefix: {self.subnet_prefix}"