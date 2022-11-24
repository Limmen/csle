
class NmapOs:
    """
    DTO representing the operating system found with an NMAP scan
    """

    def __init__(self, name: str, vendor: str, osfamily: str, accuracy: int):
        """
        Initializes the DTO object

        :param name: the name of the operating system
        :param vendor: the vendor of the operating system
        :param osfamily: the family of the operating system
        :param accuracy: the accuracy of the OS guess
        """
        self.name = name
        self.vendor = vendor
        self.osfamily = osfamily
        self.accuracy = accuracy

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"name:{self.name}, vendor:{self.vendor}, os_family:{self.osfamily}, accuracy:{self.accuracy}"

    @staticmethod
    def get_best_match(os_matches):
        """
        Returns the best matching os

        :param os_matches: list of os matches
        :return: best matching os
        """
        best_accuracy = 0
        best_os = None
        for os in os_matches:
            if os.accuracy > best_accuracy:
                best_os = os
        return best_os
