from typing import List
from csle_collector.client_manager.dao.eptmp_rate_function import EPTMPRateFunction
from csle_collector.client_manager.dao.service import Service


class Client:
    """
    A client type with an arrival process and a workflow distribution.
    """
    def __init__(self, arrival_process: EPTMPRateFunction, workflow_distribution: List[float]) -> None:
        """
        Initializes the object

        :param arrival_process: the arrival process of the client
        :param workflow_distribution: the workflow distribution of the client
        """
        self.arrival_process = arrival_process
        assert sum(workflow_distribution) == 1
        self.workflow_distribution = workflow_distribution
    
    def generate_commands(self, services: List[Service]) -> List[str]:
        """
        Generates a sequence of commands for a client of this type.
        The sequence of commands is generated according to the workflow distribution of this client type.

        :param services: A list of services that the client can use. This is the state space of the workflows in the
                         workflow distribution. It is assumed that the number of services is the same as the dimension
                         of the workflows in the workflow distribution.
                         The last service in the list is the exit service.
        :return: the list of commands
        """
        workflow = self.workflow_distribution.sample()
        commands = []
        while workflow.current_state != len(services)-1:
            commands += services[workflow.current_state].commands
            workflow.step_forward()
        # Reset workflow
        workflow.reset()
        return commands
        
        
    