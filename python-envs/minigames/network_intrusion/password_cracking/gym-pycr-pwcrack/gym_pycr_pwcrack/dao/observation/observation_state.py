
class ObservationState:

    def __init__(self, num_machines : int, num_ports : int, num_vuln : int):
        self.num_machines = num_machines
        self.num_ports = num_ports
        self.num_vuln = num_vuln
        self.machines = []
