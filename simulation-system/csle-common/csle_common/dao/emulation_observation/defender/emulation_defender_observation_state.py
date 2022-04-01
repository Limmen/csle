import time
from typing import List
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_observation.defender.emulation_defender_machine_observation_state \
    import EmulationDefenderMachineObservationState
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_collector.client_manager.client_population_metrics import ClientPopulationMetrics
from csle_collector.docker_stats_manager.docker_stats import DockerStats
from csle_collector.ids_manager.alert_counters import AlertCounters


class EmulationDefenderObservationState:
    """
    Represents the defender's agent's current belief state of the emulation
    """

    def __init__(self):
        """
        Initializes the DTO

        :param num_machines: the numer of machines
        :param ids: whether there is an IDS or not
        """
        self.machines : List[EmulationDefenderMachineObservationState] = []
        self.actions_tried = set()
        self.client_population_metrics = ClientPopulationMetrics()
        self.docker_stats = DockerStats()
        self.ids_alert_counters = AlertCounters()


    @staticmethod
    def from_dict(d: dict)-> "EmulationDefenderObservationState":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = EmulationDefenderObservationState()
        obj.machines = list(map(lambda x: EmulationDefenderMachineObservationState.from_dict(x), d["machines"]))
        obj.actions_tried = set(d["actions_tried"])
        obj.client_population_metrics = ClientPopulationMetrics.from_dict(d["client_population_metrics"])
        obj.docker_stats = DockerStats.from_dict(d["docker_stats"])
        obj.ids_alert_counters = AlertCounters.from_dict(d["ids_alert_counters"])

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["machines"] = list(map(lambda x: x.to_dict(), self.machines))
        d["actions_tried"] = list(self.actions_tried)
        d["client_population_metrics"] = self.client_population_metrics.to_dict()
        d["docker_stats"] = self.docker_stats.to_dict()
        d["ids_alert_counters"] = self.ids_alert_counters.to_dict()
        return d

    def sort_machines(self) -> None:
        """
        Sorts the machines in the observation

        :return: None
        """
        self.machines = sorted(self.machines, key=lambda x: int(x.ips[0].rsplit(".", 1)[-1]), reverse=False)

    def cleanup(self) -> None:
        """
        Cleans up the machines in the observation

        :return: None
        """
        for m in self.machines:
            m.cleanup()

    def get_action_ips(self, a : EmulationDefenderAction, emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        Gets the ips of the node that a defender action is targeted for

        :param a: the action
        :param emulation_env_config: the emulation env config
        :return: the ip of the target node
        """
        if a.index == -1:
            return emulation_env_config.topology_config.subnetwork_masks
        if a.index < len(self.machines):
            return self.machines[a.index].ips
        return a.ips

    def copy(self) -> "EmulationDefenderObservationState":
        """
        :return: a copy of the object
        """
        c = EmulationDefenderObservationState()
        c.actions_tried = self.actions_tried.copy()

        for m in self.machines:
            c.machines.append(m.copy())
        return c

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "\n".join([str(i) + ":" + str(self.machines[i]) for i in range(len(self.machines))])
