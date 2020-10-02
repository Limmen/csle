class Flag:

    def __init__(self, name:str, id:int, path:str, requires_root : bool = False, score: int = 1):
        self.name = name
        self.id = id
        self.path = path
        self.requires_root = requires_root
        self.score = score

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, Flag):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.id == other.id and self.name == other.name and self.path == other.path