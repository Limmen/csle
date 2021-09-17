
class Flag:
    """
    Class that represents a flag in the environment
    """

    def __init__(self, name:str, id:int, path:str, requires_root : bool = False, score: int = 1):
        """
        Initializes the DTO

        :param name: the name of the flag
        :param id: the id of the flag
        :param path: the path of the flag
        :param requires_root: whether the flag requires root or not
        :param score: the score of the flag
        """
        self.name = name
        self.id = id
        self.path = path
        self.requires_root = requires_root
        self.score = score

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "name:{}, id:{}, path:{}, requires_root:{}, score:{}".format(
            self.name, self.id, self.path, self.requires_root, self.score
        )

    def __hash__(self) -> int:
        """
        :return: a hash representation of the object
        """
        return hash(self.id)

    def __eq__(self, other) -> bool:
        """
        Tests equality with another flag

        :param other: the flag to compare with
        :return: True if equal otherwise False
        """
        if not isinstance(other, Flag):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.id == other.id and self.name == other.name and self.path == other.path
