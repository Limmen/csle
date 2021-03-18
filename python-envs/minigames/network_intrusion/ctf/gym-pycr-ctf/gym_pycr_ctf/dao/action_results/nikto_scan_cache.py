#import hashlib

class NiktoScanCache:

    def __init__(self):
        self.cache = {}

    def add(self, id, result):
        #id = hashlib.sha1(id.encode())
        if id not in self.cache:
            self.cache[id]= result

    def get(self, id):
        #id = hashlib.sha1(id.encode())
        if id in self.cache:
            return self.cache[id]
        return None
