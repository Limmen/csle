
class NmapHttpGrep:
    """
    A DTO representing the output of a Nmap HTTP Grep
    """

    def __init__(self, output: str):
        """
        Initializes the DTO

        :param output: the output of the HTTP Grep
        """
        self.output = output

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"output:{self.output}"
