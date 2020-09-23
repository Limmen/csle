class Flag:

    def __init__(self, name:str, id:int, path:str, requires_root : bool = False, score: int = 1):
        self.name = name
        self.id = id
        self.path = path
        self.requires_root = requires_root
        self.score = score