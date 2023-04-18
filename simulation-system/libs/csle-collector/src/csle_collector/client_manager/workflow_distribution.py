from random import choices
from typing import List, Tuple

from workflow import Workflow


class WorkflowDistribution:
    """
    A workflow distribution that represents a random variable whose outcomes consists of different workflows.
    """
    def __init__(self, workflows: List[Tuple[float, Workflow]]):
        self.workflows = workflows
    
    def sample(self):
        """
        This method was written by Bing AI.
        Returns a random workflow according to the distribution.
        """
        weights = [w[0] for w in self.workflows]
        workflows = [w[1] for w in self.workflows]
        return choices(workflows, weights=weights)[0]