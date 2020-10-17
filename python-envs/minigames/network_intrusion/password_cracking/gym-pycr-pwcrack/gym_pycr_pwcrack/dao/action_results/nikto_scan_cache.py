
class NiktoScanCache:

    def __init__(self):
        self.cache = {}

    def add(self, id, result):
        if id not in self.cache:
            self.cache[id]= result

    def get(self, id):
        if id in self.cache:
            return self.cache[id]
        return None
