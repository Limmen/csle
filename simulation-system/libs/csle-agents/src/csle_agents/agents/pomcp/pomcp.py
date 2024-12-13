from typing import List, Union, Callable, Any, Dict, Tuple
import time
import random
import torch
import math
import numpy as np
import copy
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.dao.training.policy import Policy
from csle_common.logging.log import Logger
from csle_agents.agents.pomcp.belief_tree import BeliefTree
from csle_agents.agents.pomcp.belief_node import BeliefNode
from csle_agents.agents.pomcp.action_node import ActionNode
from csle_agents.agents.pomcp.pomcp_acquisition_function_type import POMCPAcquisitionFunctionType
from csle_agents.agents.pomcp.pomcp_util import POMCPUtil
import csle_agents.constants.constants as constants


class POMCP:
    """
    Class that implements the POMCP algorithm
    """

    def __init__(self, A: List[int], gamma: float, env: BaseEnv, c: float,
                 initial_particles: List[Any], planning_time: float = 0.5, max_particles: int = 350,
                 reinvigoration: bool = False,
                 reinvigorated_particles_ratio: float = 0.1,
                 rollout_policy: Union[Policy, None] = None,
                 value_function: Union[Callable[[Any], float], None] = None, verbose: bool = False,
                 default_node_value: float = 0, prior_weight: float = 1.0, prior_confidence: int = 0,
                 acquisition_function_type: POMCPAcquisitionFunctionType = POMCPAcquisitionFunctionType.UCB,
                 c2: float = 1, use_rollout_policy: bool = False, prune_action_space: bool = False,
                 prune_size: int = 3) -> None:
        """
        Initializes the solver

        :param S: the state space
        :param A: the action space
        :param gamma: the discount factor
        :param env: the environment for sampling
        :param c: the weighting factor for UCB
        :param initial_particles: the initial list of particles
        :param planning_time: the planning time
        :param max_particles: the maximum number of particles (samples) for the belief state
        :param reinvigorated_particles_ratio: probability of new particles added when updating the belief state
        :param reinvigoration: boolean flag indicating whether reinvigoration should be done
        :param rollout_policy: the rollout policy
        :param verbose: boolean flag indicating whether logging should be verbose
        :param default_node_value: the default value of nodes in the tree
        :param num_evals_per_process: number of evaluations per process
        :param prior_weight: the weight to put on the prior
        :param prior_confidence: the prior confidence (initial count)
        :param acquisition_function_type: the type of acquisition function
        :param c2: the weighting factor for alpha go exploration
        :param use_rollout_policy: boolean flag indicating whether rollout policy should be used
        :param prune_action_space: boolean flag indicating whether the action space should be pruned
        :param prune_size: the size of the pruned action space
        """
        self.A = A
        self.env = env
        o, info = self.env.reset()
        self.root_observation = info[constants.COMMON.OBSERVATION]
        self.gamma = gamma
        self.c = c
        self.c2 = c2
        self.planning_time = planning_time
        self.max_particles = max_particles
        self.reinvigorated_particles_ratio = reinvigorated_particles_ratio
        self.rollout_policy = rollout_policy
        self.initial_visit_count = 0
        self.value_function = value_function
        self.initial_particles = initial_particles
        self.reinvigoration = reinvigoration
        self.default_node_value = default_node_value
        self.prior_weight = prior_weight
        root_particles = copy.deepcopy(self.initial_particles)
        self.tree = BeliefTree(root_particles=root_particles, default_node_value=self.default_node_value,
                               root_observation=self.root_observation, initial_visit_count=self.initial_visit_count)
        self.verbose = verbose
        self.prior_confidence = prior_confidence
        self.acquisition_function_type = acquisition_function_type
        self.use_rollout_policy = use_rollout_policy
        self.prune_action_space = prune_action_space
        self.prune_size = prune_size
        self.num_simulation_steps = 0

    def compute_belief(self) -> Dict[int, float]:
        """
        Computes the belief state based on the particles

        :return: the belief state
        """
        belief_state = {}
        particle_distribution = POMCPUtil.convert_samples_to_distribution(self.tree.root.particles)
        for state, prob in particle_distribution.items():
            belief_state[state] = round(prob, 6)
        return belief_state

    def rollout(self, state: int, history: List[int], depth: int, max_rollout_depth: int, t: int) -> float:
        """
        Perform randomized recursive rollout search starting from the given history
        until the max depth has been achieved

        :param state: the initial state of the rollout
        :param history: the history of the root node
        :param depth: current planning horizon
        :param max_rollout_depth: max rollout depth
        :param t: the time step
        :return: the estimated value of the root node
        """
        if depth > max_rollout_depth:
            if self.value_function is not None:
                o = self.env.get_observation_from_history(history=history)
                return self.value_function(o)
            else:
                return 0
        if not self.use_rollout_policy or self.rollout_policy is None or self.env.is_state_terminal(state):
            rollout_actions = self.env.get_actions_from_particles(particles=[state], t=len(history),
                                                                  observation=history[-1])
            a = POMCPUtil.rand_choice(rollout_actions)
        else:
            a = self.rollout_policy.action(o=self.env.get_observation_from_history(history=history),
                                           deterministic=False)
        self.env.set_state(state=state)
        _, r, _, _, info = self.env.step(a)
        self.num_simulation_steps += 1
        s_prime = info[constants.COMMON.STATE]
        o = info[constants.COMMON.OBSERVATION]
        return float(r) + self.gamma * self.rollout(state=s_prime, history=history + [a, o], depth=depth + 1,
                                                    max_rollout_depth=max_rollout_depth, t=t)

    def simulate(self, state: int, max_rollout_depth: int, c: float, history: List[int], t: int,
                 max_planning_depth: int, depth=0, parent: Union[None, BeliefNode, ActionNode] = None) \
            -> Tuple[float, int]:
        """
        Performs the POMCP simulation starting from a given belief node and a sampled state

        :param state: the sampled state from the belief state of the node
        :param max_rollout_depth: the maximum depth of rollout
        :param max_planning_depth: the maximum depth of planning
        :param c: the weighting factor for the ucb acquisition function
        :param depth: the current depth of the simulation
        :param history: the current history (history of the start node plus the simulation history)
        :param parent: the parent node in the tree
        :param t: the time-step
        :return: the Monte-Carlo value of the node and the current depth
        """

        # Check if we have reached the maximum depth of the tree
        if depth > max_planning_depth:
            if len(history) > 0 and self.value_function is not None:
                o = self.env.get_observation_from_history(history=history)
                return self.value_function(o), depth
            else:
                return 0, depth

        # Check if the new history has already been visited in the past of should be added as a new node to the tree
        observation = -1
        if len(history) > 0:
            observation = history[-1]
        if observation != -1 and self.value_function is not None:
            value = self.value_function(self.env.get_observation_from_history(history))
        else:
            value = self.default_node_value
        current_node = self.tree.find_or_create(history=history, parent=parent, observation=observation,
                                                initial_visit_count=self.prior_confidence, initial_value=value)
        # If a new node was created, then it has no children, in which case we should stop the search and
        # do a Monte-Carlo rollout with a given base policy to estimate the value of the node
        if len(current_node.children) == 0:
            # Prune action space
            if self.prune_action_space and self.rollout_policy is not None:
                obs_vector = self.env.get_observation_from_history(current_node.history)
                dist = self.rollout_policy.model.policy.get_distribution(
                    obs=torch.tensor([obs_vector]).to(self.rollout_policy.model.device)).log_prob(
                    torch.tensor(self.A).to(self.rollout_policy.model.device)).cpu().detach().numpy()
                dist = list(map(lambda i: (math.exp(dist[i]), self.A[i]), list(range(len(dist)))))
                rollout_actions = list(map(lambda x: x[1], sorted(dist, reverse=True,
                                                                  key=lambda x: x[0])[:self.prune_size]))
            else:
                rollout_actions = self.A
                if isinstance(current_node, BeliefNode):
                    rollout_actions = self.env.get_actions_from_particles(particles=current_node.particles + [state],
                                                                          t=t + depth, observation=observation)

            if len(current_node.children) == 0:
                # since the node does not have any children, we first add them to the node
                for action in rollout_actions:
                    self.tree.add(history + [action], parent=current_node, action=action, value=self.default_node_value)

            # Perform the rollout from the current state and return the value
            self.env.set_state(state=state)
            return (self.rollout(state=state, history=history, depth=depth, max_rollout_depth=max_rollout_depth, t=t),
                    depth)

        # If we have not yet reached a new node, we select the next action according to the acquisiton function
        if self.acquisition_function_type == POMCPAcquisitionFunctionType.UCB:
            random.shuffle(current_node.children)
            next_action_node = sorted(
                current_node.children, key=lambda x: POMCPUtil.ucb_acquisition_function(x, c=c), reverse=True)[0]
        elif self.acquisition_function_type == POMCPAcquisitionFunctionType.ALPHA_GO:
            o = self.env.get_observation_from_history(current_node.history)
            if self.rollout_policy is None:
                raise ValueError("Cannot use the AlphaGo acquisiton function without a rollout policy")
            dist = self.rollout_policy.model.policy.get_distribution(
                obs=torch.tensor([o]).to(self.rollout_policy.model.device)).log_prob(
                torch.tensor(self.A).to(self.rollout_policy.model.device)).cpu().detach().numpy()
            dist = list(map(lambda i: math.exp(dist[i]), list(range(len(dist)))))
            next_action_node_idx = sorted(
                list(range(len(current_node.children))), key=lambda x: POMCPUtil.alpha_go_acquisition_function(
                    current_node.children[x], c=c, c2=self.c2, prior=dist[x],
                    prior_weight=self.prior_weight), reverse=True)[0]
            next_action_node = current_node.children[next_action_node_idx]
        else:
            raise ValueError(f"Acquisition function type: {self.acquisition_function_type} not recognized")

        # Simulate the outcome of the selected action
        a = next_action_node.action
        self.env.set_state(state=state)
        _, r, _, _, info = self.env.step(a)
        self.num_simulation_steps += 1
        o = info[constants.COMMON.OBSERVATION]
        s_prime = info[constants.COMMON.STATE]

        # Recursive call, continue the simulation from the new node
        assert isinstance(next_action_node, ActionNode)
        R, rec_depth = self.simulate(
            state=s_prime, max_rollout_depth=max_rollout_depth, depth=depth + 1,
            history=history + [next_action_node.action, o],
            parent=next_action_node, c=c, max_planning_depth=max_planning_depth, t=t)
        R = float(r) + self.gamma * R

        # The simulation has completed, time to backpropagate the values
        # We start by updating the belief particles and the visit count of the current belief node
        if isinstance(current_node, BeliefNode):
            current_node.particles += [state]

        # Next we update the statistics and visit counts of the action node
        if isinstance(next_action_node, ActionNode):
            next_action_node.update_stats(immediate_reward=r)
        current_node.visit_count += 1
        next_action_node.visit_count += 1
        next_action_node.value += (R - next_action_node.value) / next_action_node.visit_count

        return float(R), rec_depth

    def solve(self, max_rollout_depth: int, max_planning_depth: int, t: int) -> None:
        """
        Runs the POMCP algorithm with a given max depth for the lookahead

        :param max_rollout_depth: the max depth for rollout
        :param max_planning_depth: the max depth for planning
        :return: None
        """
        if self.verbose:
            Logger.__call__().get_logger().info(
                f"Starting POMCP, max rollout depth: {max_rollout_depth}, max planning depth: {max_planning_depth}, "
                f"c: {self.c}, planning time: {self.planning_time}, gamma: {self.gamma}, "
                f"max particles: {self.max_particles}, "
                f"reinvigorated_particles_ratio: {self.reinvigorated_particles_ratio}, "
                f"prior weight: {self.prior_weight}, "
                f"acquisiton: {self.acquisition_function_type.value}, c2: {self.c2}, prune: {self.prune_action_space}, "
                f"prune size: {self.prune_size}, use_rollout_policy: {self.use_rollout_policy}, "
                f"prior confidence: {self.prior_confidence}")
        self.num_simulation_steps = 0
        begin = time.time()
        n = 0
        state = self.tree.root.sample_state()
        self.env.set_state(state)
        while time.time() - begin < self.planning_time:
            n += 1
            state = self.tree.root.sample_state()
            _, depth = self.simulate(state=state, max_rollout_depth=max_rollout_depth, history=self.tree.root.history,
                                     c=self.c,
                                     parent=self.tree.root, max_planning_depth=max_planning_depth, depth=0, t=t)
            if self.verbose:
                action_values = np.zeros((len(self.A),))
                best_action_idx = 0
                best_value = -np.inf
                counts = []
                values = []
                for i, action_node in enumerate(self.tree.root.children):
                    action_values[action_node.action] = action_node.value - 10 / (1 + action_node.visit_count)
                    if action_values[action_node.action] > best_value:
                        best_action_idx = i
                        best_value = action_values[action_node.action]
                    counts.append(action_node.visit_count)
                    values.append(round(action_values[action_node.action], 1))
                Logger.__call__().get_logger().info(
                    f"Planning time left {self.planning_time - time.time() + begin}s, "
                    f"best action: {self.tree.root.children[best_action_idx].action}, "
                    f"value: {self.tree.root.children[best_action_idx].value}, "
                    f"count: {self.tree.root.children[best_action_idx].visit_count}, "
                    f"planning depth: {depth}, counts: "
                    f"{sorted(counts, reverse=True)[0:5]}, values: {sorted(values, reverse=True)[0:5]}")
        if self.verbose:
            Logger.__call__().get_logger().info(f"Planning complete, num simulation steps: {self.num_simulation_steps}")

    def get_action(self) -> int:
        """
        Gets the next action to execute based on the state of the tree. Selects the action with the highest value
        from the root node.

        :return: the next action
        """
        root = self.tree.root
        action_vals = [(action.value - 10 / (action.visit_count + 1), action.action) for action in root.children]
        if self.verbose:
            for a in root.children:
                Logger.__call__().get_logger().info(f"action: {a.action}, value: {a.value}, "
                                                    f"visit count: {a.visit_count}")
        return int(max(action_vals)[1])

    def update_tree_with_new_samples(self, action_sequence: List[int], observation: int, t: int) -> List[Any]:
        """
        Updates the tree after an action has been selected and a new observation been received

        :param action_sequence: the action sequence that was executed
        :param observation: the observation that was received
        :param t: the time-step
        :return: the updated particle state
        """
        root = self.tree.root
        if len(action_sequence) == 0:
            raise ValueError("Invalid action sequence")
        action = action_sequence[-1]

        # Since we executed an action we advance the tree and update the root to the the node corresponding to the
        # action that was selected
        child = root.get_child(action)
        if child is not None:
            new_root = child.get_child(observation)
        else:
            raise ValueError(f"Could not find child node for action: {action}")

        # If we did not have a node in the tree corresponding to the observation that was observed, we select a random
        # belief node to be the new root (note that the action child node will always exist by definition of the
        # algorithm)
        if new_root is None:
            # Get the action node
            action_node = root.get_child(action)
            if action_node is None:
                raise ValueError("Chould not find the action node")

            if action_node.children:
                # If the action node has belief state nodes, select a random of them to be the new root
                new_root = POMCPUtil.rand_choice(action_node.children)
            else:
                # or create the new belief node randomly
                particles = copy.deepcopy(self.initial_particles)
                if self.value_function is not None:
                    # initial_value = self.value_function(observation)
                    initial_value = self.default_node_value
                else:
                    initial_value = self.default_node_value
                new_root = self.tree.add(history=action_node.history + [observation], parent=action_node,
                                         observation=observation, particle=particles, value=initial_value,
                                         initial_visit_count=self.prior_confidence)

        # Check how many new particles are left to fill
        if isinstance(new_root, BeliefNode):
            new_root.particles = []
            particle_slots = self.max_particles - len(new_root.particles)
        else:
            raise ValueError("Invalid root node")
        if particle_slots > 0:
            if self.verbose:
                Logger.__call__().get_logger().info(f"Filling {particle_slots} particles")
            particles = []
            # fill particles by Monte-Carlo using reject sampling
            count = 0
            while len(particles) < particle_slots:
                s = root.sample_state()
                self.env.set_state(state=s)
                _, r, _, _, info = self.env.step(action)
                s_prime = info[constants.COMMON.STATE]
                o = info[constants.COMMON.OBSERVATION]
                if o == observation:
                    particles.append(s_prime)
                    count = 0
                else:
                    count += 1
                if count >= 50000:
                    target = root.sample_state().red_agent_target
                    Logger.__call__().get_logger().info(
                        f"Invalid observation: {observation}, target: {target}, "
                        f"given state: 1: \n{root.sample_state()}, \n"
                        f"2: \n {root.sample_state()}\n, 3: {root.sample_state()}\n ")
                    for i in range(particle_slots - len(particles)):
                        s = root.sample_state()
                        self.env.set_state(state=s)
                        _, r, _, _, info = self.env.step(action)
                        s_prime = info[constants.COMMON.STATE]
                        particles.append(s_prime)

            new_root.particles += particles

        # We now prune the old root from the tree
        self.tree.prune(root, exclude=new_root)
        # and update the root
        self.tree.root = new_root

        # Prune children
        if self.verbose:
            Logger.__call__().get_logger().info("Pruning children")
        feasible_actions = (
            self.env.get_actions_from_particles(particles=self.tree.root.particles, t=t, observation=observation,
                                                verbose=True))
        if self.verbose:
            Logger.__call__().get_logger().info(f"feasible actions: {feasible_actions}")
        children = []
        for ch in self.tree.root.children:
            if ch.action in feasible_actions:
                children.append(ch)
        self.tree.root.children = children

        # To avoid particle deprivation (i.e., that the algorithm gets stuck with the wrong belief)
        # we do particle reinvigoration here
        if self.reinvigoration and len(self.initial_particles) > 0:
            if self.verbose:
                Logger.__call__().get_logger().info("Starting reinvigoration")

            # Generate some new particles randomly
            num_reinvigorated_particles = int(len(new_root.particles) * self.reinvigorated_particles_ratio)
            reinvigorated_particles = []
            for i in range(num_reinvigorated_particles):
                s = root.sample_state()
                self.env.set_state(state=s)
                _, r, _, _, info = self.env.step(action)
                s_prime = info[constants.COMMON.STATE]
                reinvigorated_particles.append(s_prime)

            # Randomly exchange some old particles for the new ones
            for particle in reinvigorated_particles:
                new_root.particles[np.random.randint(0, len(new_root.particles))] = particle
        return new_root.particles
