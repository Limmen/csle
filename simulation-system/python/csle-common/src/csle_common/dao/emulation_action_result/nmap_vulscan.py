
class NmapVulscan:
    """
    DTO representing the result of a NMAP Vulscan
    """

    def __init__(self, output: str):
        """
        Intializes the DTO

        :param output: the output of the scan
        """
        self.output = output

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"output:{self.output}"
