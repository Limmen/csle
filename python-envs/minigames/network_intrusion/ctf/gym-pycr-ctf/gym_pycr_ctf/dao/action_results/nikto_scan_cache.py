

class NiktoScanCache:
    """
    Object representing the cache of Nikto-scan results
    """

    def __init__(self):
        """
        Initializes the cache
        """
        self.cache = {}

    def add(self, id : str, result) -> None:
        """
        Adds a result to the cache

        :param id: the cache id
        :param result: the cache result
        :return: None
        """
        if id not in self.cache:
            self.cache[id]= result

    def get(self, id : str):
        """
        Gets the cached result of a given cache id

        :param id: id of the cache entry
        :return: the cached result
        """
        if id in self.cache:
            return self.cache[id]
        return None
