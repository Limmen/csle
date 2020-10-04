from typing import List
from gym_pycr_pwcrack.dao.observation.machine_observation_state import MachineObservationState

class ObservationState:

    def __init__(self, num_machines : int, num_ports : int, num_vuln : int, num_sh : int,
                 num_flags : int, catched_flags : int):
        self.num_machines = num_machines
        self.num_ports = num_ports
        self.num_vuln = num_vuln
        self.machines : List[MachineObservationState] = []
        self.detected = False
        self.all_flags = False
        self.num_sh = num_sh
        self.num_flags = num_flags
        self.catched_flags = 0


    def sort_machines(self):
        self.machines = sorted(self.machines, key=lambda x: int(x.ip.rsplit(".", 1)[-1]), reverse=False)
