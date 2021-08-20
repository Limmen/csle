
class FileSystemScanCache:
    """
    Object for managing the cache of file system scans
    """

    def __init__(self):
        """
        Initializes the objet
        """
        self.cache = {}

    def add(self, id : str, result) -> None:
        """
        Adds a cached result to the cache

        :param id: the id of the result
        :param result: the result
        :return: None
        """
        if id not in self.cache:
            self.cache[id]= result

    def get(self, id : str):
        """
        Gets the result of a given id from the cache

        :param id: the id of the cache entry
        :return: the cached result
        """
        if id in self.cache:
            return self.cache[id]
        return None
