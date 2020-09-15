
class MachineObservationState:

    def __init__(self, ip : str):
        self.ip = ip
        self.os="unknown"
        self.ports = []
        self.vuln = []