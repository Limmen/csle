
class UserCommandCache:
    """
    Class representing the cache of user commands
    """

    def __init__(self):
        """
        Initializes the cache
        """
        self.cache = {}

    def add(self, id : str, result) -> None:
        """
        Adds a result to the cache

        :param id: the id of the cache entry
        :param result: the result to add to the cache entry
        :return: None
        """
        if id not in self.cache:
            self.cache[id]= result

    def get(self, id):
        """
        Gets the result value of a cache entry

        :param id: the id of the cache entry
        :return: the result if it exists or otherwise None
        """
        if id in self.cache:
            return self.cache[id]
        return None
