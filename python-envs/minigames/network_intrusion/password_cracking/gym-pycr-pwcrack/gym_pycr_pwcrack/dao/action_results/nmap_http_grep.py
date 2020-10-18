
class NmapHttpGrep:

    def __init__(self, output : str):
        self.output = output

    def __str__(self):
        return "output:{}".format(self.output)