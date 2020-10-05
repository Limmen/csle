from typing import List
from gym_pycr_pwcrack.dao.observation.machine_observation_state import MachineObservationState
from gym_pycr_pwcrack.dao.action.action import Action

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
        self.catched_flags = catched_flags


    def sort_machines(self):
        self.machines = sorted(self.machines, key=lambda x: int(x.ip.rsplit(".", 1)[-1]), reverse=False)


    def cleanup(self):
        for m in self.machines:
            m.cleanup()


    def get_action_id(self, a : Action):
        if a.index < len(self.machines) and a.index != -1:
            self.sort_machines()
            return self.machines[a.index].ip
        return a.ip
