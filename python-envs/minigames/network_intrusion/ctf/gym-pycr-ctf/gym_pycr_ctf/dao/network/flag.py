class Flag:

    def __init__(self, name:str, id:int, path:str, requires_root : bool = False, score: int = 1):
        self.name = name
        self.id = id
        self.path = path
        self.requires_root = requires_root
        self.score = score

    def __str__(self):
        return "name:{}, id:{}, path:{}, requires_root:{}, score:{}".format(
            self.name, self.id, self.path, self.requires_root, self.score
        )

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, Flag):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.id == other.id and self.name == other.name and self.path == other.path

    def __hash__(self):
        return hash(self.id) + 31 * hash(self.name) + 31 * hash(self.path)