from typing import List
from gym_pycr_pwcrack.dao.observation.machine_observation_state import MachineObservationState

class ObservationState:

    def __init__(self, num_machines : int, num_ports : int, num_vuln : int):
        self.num_machines = num_machines
        self.num_ports = num_ports
        self.num_vuln = num_vuln
        self.machines : List[MachineObservationState] = []


    def sort_machines(self):
        self.machines = sorted(self.machines, key=lambda x: int(x.ip.rsplit(".", 1)[-1]), reverse=False)
