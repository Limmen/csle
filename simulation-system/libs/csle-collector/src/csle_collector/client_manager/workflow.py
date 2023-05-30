import random
from typing import List

import numpy as np

class Workflow:
    """
    A Markov chain representation of a workflow.
    """
    def __init__(self, transition_matrix: List[List[float]], initial_state: int):
        self.transition_matrix = transition_matrix
        self.initial_state = initial_state
        self.current_state = initial_state
        self.t = 0
    
    def step_forward(self) -> int:
        """
        Move t forward by one and possibly transition to a new state.
        Returns the new state.
        """
        self.t += 1
        next_state = markov_next_state(row=self.transition_matrix[self.current_state])
        self.current_state = next_state
        return self.current_state
    
    def reset(self):
        self.current_state = self.initial_state
        self.t = 0

def markov_next_state(row):
    """ 
    This method was written by Bing AI.
    Row is a numpy array of probabilities that sum up to 1.
    Returns an integer from 0 to len(row)-1.
    """
    cumsum = np.cumsum(row) # cumulative sum of probabilities
    r = random.random() # random number between 0 and 1
    for i in range(len(cumsum)):
        if r < cumsum[i]: # find the first index where r is smaller than cumsum[i]
            return i # return that index as the outcome