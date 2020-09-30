
class NmapOs:

    def __init__(self, name : str, vendor: str, osfamily: str, accuracy: int):
        self.name = name
        self.vendor = vendor
        self.osfamily = osfamily
        self.accuracy = accuracy


    def __str__(self):
        return "name:{}, vendor:{}, os_family:{}, accuracy:{}".format(self.name, self.vendor, self.osfamily,
                                                                      self.accuracy)

    @staticmethod
    def get_best_match(os_matches):
        best_accuracy = 0
        best_os = None
        for os in os_matches:
            if os.accuracy > best_accuracy:
                best_os = os
        return best_os