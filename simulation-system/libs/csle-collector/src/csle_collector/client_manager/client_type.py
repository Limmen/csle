from typing import List
from csle_collector.client_manager.eptmp_rate_function import EPTMPRateFunction
from csle_collector.client_manager.service import Service
import logging

from csle_collector.client_manager.workflow_distribution import WorkflowDistribution


class ClientType:
    """
    A client type with an arrival process and a workflow distribution.
    """
    def __init__(self, arrival_process: EPTMPRateFunction, workflow_distribution: WorkflowDistribution):
        self.arrival_process = arrival_process
        self.workflow_distribution = workflow_distribution
    
    def generate_commands(self, services: List[Service]):
        """
        Generates a sequence of commands for a client of this type.
        The sequence of commands is generated according to the workflow distribution of this client type.

        :param services: A list of services that the client can use. This is the state space of the workflows in the workflow distribution.
                         It is assumed that the number of services is the same as the dimension of the workflows in the workflow distribution.
                         The last service in the list is the exit service.
        """
        workflow = self.workflow_distribution.sample()
        commands = []
        while workflow.current_state != len(services)-1:
            logging.info("workflow.current_state: " + str(workflow.current_state) + "length services: " + str(len(services)))
            commands += services[workflow.current_state].commands
            workflow.step_forward()

        # Reset workflow
        workflow.reset()
        return commands
        
        
    