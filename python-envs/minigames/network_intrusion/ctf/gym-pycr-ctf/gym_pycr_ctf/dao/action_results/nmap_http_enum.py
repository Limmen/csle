
class NmapHttpEnum:
    """
    DTO representing a NMAP HTTP Enum
    """

    def __init__(self, output : str):
        """
        Initializes the DTO

        :param output: the output of the HTTP enum
        """
        self.output = output

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "output:{}".format(self.output)