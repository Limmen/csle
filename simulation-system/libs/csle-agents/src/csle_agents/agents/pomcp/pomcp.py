from typing import List, Union
import time
import numpy as np
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.dao.training.policy import Policy
from csle_agents.agents.pomcp.belief_tree import BeliefTree
from csle_agents.agents.pomcp.belief_node import BeliefNode
from csle_agents.agents.pomcp.action_node import ActionNode
from csle_agents.agents.pomcp.pomcp_util import POMCPUtil
import csle_agents.constants.constants as constants


class POMCP:
    """
    Class that implements the POMCP algorithm
    """

    def __init__(self, S: List[int], O: List[int], A: List[int], gamma: float, env: BaseEnv, c: float,
                 initial_belief: List[float], planning_time: float = 0.5, max_particles: int = 350,
                 reinvigorated_particles_ratio: float = 0.1, rollout_policy: Union[Policy, None] = None) -> None:
        """
        Initializes the solver

        :param S: the state space
        :param O: the observation space
        :param A: the action space
        :param gamma: the discount factor
        :param env: the environment for sampling
        :param c: the weighting factor for UCB
        :param initial_belief: the initial belief state
        :param planning_time: the planning time
        :param max_particles: the maximum number of particles (samples) for the belief state
        :param reinvigorated_particles_ratio: probability of new particles added when updating the belief state
        :param rollout_policy: the rollout policy
        """
        self.S = S
        self.O = O
        self.A = A
        self.env = env
        self.gamma = gamma
        self.c = c
        self.planning_time = planning_time
        self.max_particles = max_particles
        self.reinvigorated_particles_ratio = reinvigorated_particles_ratio
        self.rollout_policy = rollout_policy
        root_particles = POMCPUtil.generate_particles(
            states=self.S, num_particles=self.max_particles, probability_vector=initial_belief)
        self.tree = BeliefTree(root_particles=root_particles)

    def compute_belief(self) -> List[float]:
        """
        Computes the belief state based on the particles

        :return: the belief state
        """
        belief_state = [0.0] * len(self.S)
        particle_distribution = POMCPUtil.convert_samples_to_distribution(self.tree.root.particles)
        for state, prob in particle_distribution.items():
            belief_state[list(self.S).index(state)] = round(prob, 6)
        return belief_state

    def rollout(self, state: int, history: List[int], depth: int, max_depth: int) -> float:
        """
        Perform randomized recursive rollout search starting from the given history
        until the max depth has been achieved

        :param state: the initial state of the rollout
        :param history: the history of the root node
        :param depth: current planning horizon
        :param max_depth: max planning horizon
        :return: the estimated value of the root node
        """
        if depth > max_depth:
            return 0
        if self.rollout_policy is None:
            a = POMCPUtil.rand_choice(self.A)
        else:
            a = self.rollout_policy.action(o=self.env.get_observation_from_history(history=history))
        self.env.set_state(state=state)
        _, r, _, _, info = self.env.step(a)
        s_prime = info[constants.COMMON.STATE]
        o = info[constants.COMMON.OBSERVATION]
        return float(r) + self.gamma * self.rollout(state=s_prime, history=history + [a, o], depth=depth + 1,
                                                    max_depth=max_depth)

    def simulate(self, state: int, max_depth: int, c: float, depth=0, history: Union[List[int], None] = None,
                 parent=Union[None, BeliefNode, ActionNode]) -> float:
        """
        Performs the POMCP simulation starting from a given belief node and a sampled state

        :param state: the sampled state from the belief state of the node
        :param max_depth: the maximum depth of the simulation
        :param c: the weighting factor for the ucb acquisition function
        :param depth: the current depth of the simulation
        :param history: the current history (history of the start node plus the simulation history)
        :param parent: the parent node in the tree
        :return: the Monte-Carlo value of the node
        """

        # Check if we have reached the maximum depth of the tree
        if depth > max_depth:
            return 0

        # Check if the new history has already been visited in the past of should be added as a new node to the tree
        obs_h = None
        if history is not None and len(history) > 0:
            obs_h = history[-1]
        current_node = self.tree.find_or_create(history=history, parent=parent, observation=obs_h)

        # If a new node was created, then it has no children, in which case we should stop the search and
        # do a Monte-Carlo rollout with a given base policy to estimate the value of the node
        if not current_node.children:
            # since the node does not have any children, we first add them to the node
            for action in self.A:
                self.tree.add(history + [action], parent=current_node, action=action)
            # Perform the rollout and return the value
            return self.rollout(state, history, depth, max_depth)

        # If we have not yet reached a new node, we select the next action according to the
        # UCB strategy
        np.random.shuffle(current_node.children)
        next_action_node = sorted(current_node.children,
                                  key=lambda x: POMCPUtil.ucb_acquisition_function(x, c=c), reverse=True)[0]

        # Simulate the outcome of the selected action
        a = next_action_node.action
        self.env.set_state(state=state)
        _, r, _, _, info = self.env.step(a)
        o = info[constants.COMMON.OBSERVATION]
        s_prime = info[constants.COMMON.STATE]

        # Recursive call, continue the simulation from the new node
        R = float(r) + self.gamma * self.simulate(
            state=s_prime, max_depth=max_depth, depth=depth + 1, history=history + [next_action_node.action, o],
            parent=next_action_node, c=c)

        # The simulation has completed, time to backpropagate the values
        # We start by updating the belief particles and the visit count of the current belief node
        current_node.particles += [state]
        current_node.visit_count += 1

        # Next we update the statistics and visit counts of the action node
        next_action_node.update_stats(immediate_reward=r)
        next_action_node.visit_count += 1
        next_action_node.value += (R - next_action_node.value) / next_action_node.visit_count

        return R

    def solve(self, max_depth: int) -> None:
        """
        Runs the POMCP algorithm with a given max depth for the lookahead

        :param max_depth: the max depth for the lookahead
        :return: None
        """
        begin = time.time()
        n = 0
        while time.time() - begin < self.planning_time:
            n += 1
            state = self.tree.root.sample_state()
            self.simulate(state, max_depth=max_depth, history=self.tree.root.history, c=self.c)

    def get_action(self) -> int:
        """
        Gets the next action to execute based on the state of the tree. Selects the action with the highest value
        from the root node.

        :return: the next action
        """
        root = self.tree.root
        action_vals = [(action.value, action.action) for action in root.children]
        return max(action_vals)[1]

    def update_tree_with_new_samples(self, action: int, observation: int) -> List[float]:
        """
        Updates the tree after an action has been selected and a new observation been received

        :param action: the action that was executed
        :param observation: the observation that was received
        :return: the updated belief state
        """
        root = self.tree.root

        # Since we executed an action we advance the tree and update the root to the the node corresponding to the
        # action that was selected
        new_root = root.get_child(action).get_child(observation)

        # If we did not have a node in the tree corresponding to the observation that was observed, we select a random
        # belief node to be the new root (note that the action child node will always exist by definition of the
        # algorithm)
        if new_root is None:
            # Get the action node
            action_node = root.get_child(action)

            if action_node.children:
                # If the action node has belief state nodes, select a random of them to be the new root
                new_root = POMCPUtil.rand_choice(action_node.children)
            else:
                # or create the new belief node randomly
                particles = POMCPUtil.generate_particles(states=self.S, num_particles=self.max_particles,
                                                         probability_vector=None)
                new_root = self.tree.add(history=action_node.history + [observation], parent=action_node,
                                         observation=observation, particle=particles)

        # Check how many new particles are left to fill
        particle_slots = self.max_particles - len(new_root.particles)
        if particle_slots > 0:
            # fill particles by Monte-Carlo using reject sampling
            particles = []
            while len(particles) < particle_slots:
                s = root.sample_state()
                self.env.set_state(state=s)
                _, r, _, _, info = self.env.step(action)
                s_prime = info[constants.COMMON.STATE]
                o = info[constants.COMMON.OBSERVATION]
                if o == observation:
                    particles.append(s_prime)
            new_root.particles += particles

        # We now prune the old root from the tree
        self.tree.prune(root, exclude=new_root)
        # and update the root
        self.tree.root = new_root
        # and compute the new belief based on the updated particles
        new_belief = self.compute_belief()

        # To avoid particle deprivation (i.e., that the algorithm gets stuck with the wrong belief)
        # we do particle reinvigoration here
        if any([prob == 0.0 for prob in new_belief]):
            # Generate same new particles randomly
            mutations = POMCPUtil.generate_particles(
                states=self.S, num_particles=int(self.max_particles * self.reinvigorated_particles_ratio),
                probability_vector=None)

            # Randomly exchange some old particles for the new ones
            for particle in mutations:
                new_root.particles[np.random.randint(0, len(new_root.particles))] = particle

            # re-compute the current belief distribution after reinvigoration
            new_belief = self.compute_belief()
        return new_belief