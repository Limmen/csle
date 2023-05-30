from random import choices
from typing import List, Tuple
from csle_collector.client_manager.workflows.workflow import Workflow


class WorkflowDistribution:
    """
    A workflow distribution that represents a random variable whose outcomes consists of different workflows.
    """
    def __init__(self, workflows: List[Tuple[float, Workflow]]) -> None:
        """
        Initializes the object

        :param workflows: the list of workflows
        """
        self.workflows = workflows
    
    def sample(self) -> Workflow:
        """
        Samples a workflow from the distribution

        :return: a sampled workflow
        """
        weights = [w[0] for w in self.workflows]
        workflows = [w[1] for w in self.workflows]
        return choices(workflows, weights=weights)[0]