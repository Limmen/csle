from typing import List
from gym_pycr_ctf.dao.action.defender.defender_action DefenderAction
from gym_pycr_ctf.dao.observation.defender_machine_observation_state import DefenderMachineObservationState


class DefenderObservationState:
    """
    Represents the defender's agent's current belief state of the environment
    """

    def __init__(self, num_machines : int, ids = False):
        self.num_machines = num_machines
        self.ids = ids
        self.machines : List[DefenderMachineObservationState] = []
        self.defense_actions_tried = set()
        self.num_alerts_recent = 0
        self.num_severe_alerts_recent = 0
        self.num_warning_alerts_recent = 0
        self.sum_priority_alerts_recent = 0
        self.num_alerts_total = 0
        self.sum_priority_alerts_total = 0
        self.num_severe_alerts_total = 0
        self.num_warning_alerts_total = 0


    def sort_machines(self):
        self.machines = sorted(self.machines, key=lambda x: int(x.ip.rsplit(".", 1)[-1]), reverse=False)

    def cleanup(self):
        for m in self.machines:
            m.cleanup()


    def get_action_ip(self, a : DefenderAction):
        if a.index == -1:
            self.sort_machines()
            ips = list(map(lambda x: x.ip, self.machines))
            ips_str = "_".join(ips)
            return ips_str
        if a.index < len(self.machines) and a.index < self.num_machines:
            return self.machines[a.index].ip
        return a.ip


    def copy(self):
        c = DefenderObservationState(num_machines = self.num_machines, ids=self.ids)
        c.defense_actions_tried = self.defense_actions_tried.copy()
        c.num_alerts_recent = self.num_alerts_recent
        c.num_severe_alerts_recent = self.num_severe_alerts_recent
        c.num_warning_alerts_recent = self.num_warning_alerts_recent
        c.sum_priority_alerts_recent = self.sum_priority_alerts_recent
        c.num_alerts_total = self.num_alerts_total
        c.num_severe_alerts_total = self.num_severe_alerts_total
        c.num_warning_alerts_total = self.num_warning_alerts_total
        c.sum_priority_alerts_total = self.sum_priority_alerts_total
        for m in self.machines:
            c.machines.append(m.copy())
        return c


    def __str__(self):
        return  "# alerts recent:{}, # severe alerts recent: {}, # warning alerts recent: {}, " \
                "sum priority recent:{}, # alerts total:{} # severe alerts total: {}, " \
                "# warning alerts total: {}, sum priority total: {}".format(
            self.num_alerts_recent, self.num_severe_alerts_recent, self.num_warning_alerts_recent,
            self.sum_priority_alerts_recent, self.num_alerts_total, self.num_severe_alerts_total,
            self.num_warning_alerts_total, self.sum_priority_alerts_total) + "\n" + \
                "\n".join([str(i) + ":" + str(self.machines[i]) for i in range(len(self.machines))])
