from typing import List, Any, Dict, Union
import time
import numpy as np
import numpy.typing as npt
from abc import abstractmethod
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.dao.stopping_game_defender_pomdp_config import StoppingGameDefenderPomdpConfig
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from gym_csle_stopping_game.envs.stopping_game_pomdp_defender_env import StoppingGamePomdpDefenderEnv
from csle_common.dao.training.random_policy import RandomPolicy
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.simulation_config.base_env import BaseEnv
import csle_agents.constants.constants as constants
from collections import Counter


def simulate_action(transition_tensor, states, observations, observation_tensor, reward_tensor,
                    si, ai, a2, l):
    """
    Query the resultant new state, observation and rewards, if action ai is taken from state si

    si: current state
    ai: action taken at the current state
    return: next state, observation and reward
    """
    # get new state
    s_probs = [transition_tensor[l][ai][a2][si][sj] for sj in states]
    state = states[sample_from_distribution(s_probs)]

    # get new observation
    o_probs = [observation_tensor[ai][a2][state][oj] for oj in observations]
    observation = observations[sample_from_distribution(o_probs)]

    # get new reward
    # reward = self.reward_function(ai, si, sj, observation) #  --- THIS IS MORE GENERAL!
    reward = reward_tensor[l][ai][a2][si]
    return state, observation, reward


def sample_from_distribution(probability_vector: List[float]) -> npt.NDArray[float]:
    """
    Utility function to normalize a probability vector and avoid numpy floating point issues

    :param probability_vector: the probability vector to normalize
    :return: the normalized vector
    """
    probability_vector = np.array(probability_vector)
    return np.random.choice(list(range(len(probability_vector))), p=probability_vector / probability_vector.sum())


def rand_choice(candidates: List[int]) -> int:
    """
    Selects an element from a given list uniformly at random

    :param candidates: the list to sample from
    :return: the sample
    """
    return np.random.choice(candidates)


def convert_samples_to_distribution(samples) -> Dict[int, float]:
    """
    Converts a list of samples to a probability distribution

    :param samples: the list of samples
    :return: a dict with the sample values and their probabilities
    """
    cnt = Counter(samples)
    _sum = sum(cnt.values())
    return {k: v / _sum for k, v in cnt.items()}


def generate_particles(states: List[int], num_particles: int, probability_vector: Union[None, List[float]]):
    """
    Generates a list of particles (sample states) for a given list of states
    with a frequency determined by a given probability vector

    :param states: the
    :param n:
    :param probability_vector: (optional) probability vector to determine the frequency of each sample
    :return:
    """
    # by default use uniform distribution for particles generation
    if probability_vector is None:
        probability_vector = [1 / len(states)] * len(states)
    return [states[sample_from_distribution(probability_vector)] for _ in range(num_particles)]


def ucb(history_visit_count, action_visit_count):
    """
    Implements the upper-confidence-bound acquisiton function

    :param history_visit_count: counter of the number of times the history has been visited
    :param action_visit_count: counter of the number of times the action has been taken in the history
    :return: the ucb acquisition value
    """
    # If we have never seen this history before, its utility is initialized to zero
    if history_visit_count == 0:
        return 0.0
    # If we have never taken this action before, its utility is infinity to encourage exploration
    if action_visit_count == 0:
        return np.inf
    # If we have taken this action before, return the UCB exploration bonus
    return np.sqrt(np.log(history_visit_count) / action_visit_count)


class Node:
    """
    Abstract node type, represents a node in the lookahead tree
    """

    def __init__(self, id: int, history: List[int], parent=None, value: float = 0, visit_count: int = 0) -> None:
        """
        Initializes the node

        :param id: the id of the node
        :param history: the history of the node
        :param parent: the parent node
        :param V: the value of the node
        :param visit_count: the visit count of the node
        """
        self.history = history
        self.value = value
        self.visit_count = visit_count
        self.id = id
        self.parent = parent
        self.children = []

    @abstractmethod
    def add_child(self, node: "Node") -> None:
        """
        Method that adds a child to the node. Should be implemented by classes that inherit from this class

        :param node: the node to add
        :return: None
        """
        pass

    @abstractmethod
    def get_child(self, *args) -> "Node":
        """
        Method that gets the child to the node. Should be implemented by classes that inherit from this class

        :param args: list of arguments to specify the child
        :return: the child
        """
        pass


class BeliefNode(Node):
    """
    Represents a node that holds the belief distribution given its history sequence in a belief tree.
    It also holds the received observation after which the belief is updated accordingly
    """

    def __init__(self, id: int, history: List[int], observation: int, parent=None, value: float = 0.0,
                 visit_count: int = 0) -> None:
        """
        Initializing the node

        :param id: the id of the node
        :param h: the history of the node
        :param observation: the latest observation
        :param parent: the parent node
        :param value: the value of the node (mean return of all simulations starting from this node)
        :param visit_count: the number of times the node has been visited in simulations
        """
        Node.__init__(self, id=id, history=history, parent=parent, value=value, visit_count=visit_count)
        self.observation = observation
        self.particles = []
        self.action_to_node_map: Dict[int, ActionNode] = {}

    def add_child(self, node: "ActionNode") -> None:
        """
        Adds a child node to this node. Since an observation is always followed by an action in the history, the next
        node will be an action node

        :param node: the child action node
        :return: None
        """
        self.children.append(node)
        self.action_to_node_map[node.action] = node

    def get_child(self, action: int) -> Union["ActionNode", None]:
        """
        Gets the child node corresponding to a specific action

        :param action: the action to get the node for
        :return: the node or None if it was not found
        """
        return self.action_to_node_map.get(action, None)

    def sample_state(self) -> int:
        """
        Samples a state from the belief state

        :return: the sampled state
        """
        return rand_choice(self.particles)

    def add_particle(self, particle: Union[int, List[int]]) -> None:
        """
        Adds a paticle (a sample state) to the list of particles

        :param particle: the particle to add
        :return: None
        """
        if type(particle) is list:
            self.particles.extend(particle)
        else:
            self.particles.append(particle)


class ActionNode(Node):
    """
    A node in the POMCP history tree where the last element of the history was an action
    """

    def __init__(self, id: int, history: List[int], action: int, parent=None, value: float = 0.0,
                 visit_count: int = 0) -> None:
        """
        Initializes the node

        :param id: the id of the node
        :param history: the history of the node
        :param action: the action of the node
        :param parent: the parent node
        :param value: the value of the node
        :param visit_count: the visit count of the node
        """
        Node.__init__(self, id=id, history=history, parent=parent, value=value, visit_count=visit_count)
        self.mean_immediate_reward: float = 0.0
        self.action: int = action
        self.observation_to_node_map: Dict[int, BeliefNode] = {}

    def update_stats(self, immediate_reward: float) -> None:
        """
        Updates the mean return from the node by computing the rolling average

        :param immediate_reward: the latest reward sample
        :return: None
        """
        self.mean_immediate_reward = (self.mean_immediate_reward * self.visit_count + immediate_reward) / \
                                     (self.visit_count + 1)

    def add_child(self, node: "BeliefNode") -> None:
        """
        Adds a child node to the tree. Since an action is always followed by an observation in the history, the next
        node will be an observation/belief node

        :param node: the new child node to add
        :return: None
        """
        self.children.append(node)
        self.observation_to_node_map[node.observation] = node

    def get_child(self, observation: int) -> Union[None, BeliefNode]:
        """
        Gets the child node corresponding to a specific observation

        :param observation: the observation to get the node for
        :return: the child node or None if it was not found
        """
        return self.observation_to_node_map.get(observation, None)


def ucb_acquisition_function(action: ActionNode, c: float) -> float:
    """
    The UCB acquisition function

    :param action: the action
    :param c: the exploration parameter
    :return: the acquisition value of the action
    """
    return action.value + c * ucb(action.parent.visit_count, action.visit_count)


class BeliefTree:
    """
    The belief tree of POMCP. Each node in the tree corresponds to a history of the POMDP, where a history is a sequence
    of actions and observations.
    """

    def __init__(self, root_particles: List[int]) -> None:
        """
        Initializes the tree with a belief node with a set of particles

        :param root_particles: the particles to add to the root belief node
        """
        self.tree_size = 0
        self.nodes = {}
        self.root = self.add(history=[], particle=root_particles, parent=None)

    def add(self, history: List[int], parent: Union[ActionNode, BeliefNode, None], action: Union[int, None] = None,
            observation: Union[int, None] = None, particle: Union[Any, None] = None):
        """
        Creates and adds a new belief node or action node to the belief search tree

        :param h: history sequence
        :param parent: either ActionNode or BeliefNode
        :param action: action
        :param observation: observation
        :param particle: new node's particle set
        :param cost: action cost of an action node
        :return:
        """
        # Create the node
        if action is not None:
            new_node = ActionNode(self.tree_size, history, parent=parent, action=action)
        else:
            new_node = BeliefNode(self.tree_size, history, parent=parent, observation=observation)

        if particle is not None:
            new_node.add_particle(particle)

        # add the node to belief tree
        self.nodes[new_node.id] = new_node
        self.tree_size += 1

        # register node as parent's child
        if parent is not None:
            parent.add_child(node=new_node)
        return new_node

    def find_or_create(self, history: List[int], parent: Union[None, BeliefNode, ActionNode], observation: int):
        """
        Search for the node corresponds to given history, otherwise create one using given params
        """
        # Start the search from the root node
        current_node = self.root

        # Start from the root node and then traverse down to the depth of the given history to see if the node
        # of this history  exists or not, otherwise add it
        history_length, root_history_length = len(history), len(self.root.history)
        for step in range(root_history_length, history_length):
            current_node = current_node.get_child(history[step])

            # Node of this history does not exists so we add it
            if current_node is None:
                return self.add(history=history, parent=parent, observation=observation)
        return current_node

    def prune(self, node, exclude=None):
        """
        Removes the entire subtree subscribed to 'node' with exceptions.
        :param node: root of the subtree to be removed
        :param exclude: exception component
        :return:
        """
        for child in node.children:
            if exclude and exclude.id != child.id:
                self.prune(child, exclude)

        self.nodes[node.id] = None
        del self.nodes[node.id]


class POMCP:
    """
    Class that implements the POMCP algorithm
    """

    def __init__(self, S: List[int], O: List[int], A: List[int], gamma: float, env: BaseEnv, c: float,
                 initial_belief: List[float], planning_time: float = 0.5, max_particles: int = 350,
                 reinvigorated_particles_ratio: float = 0.1) -> None:
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
        root_particles = generate_particles(
            states=self.S, num_particles=self.max_particles, probability_vector=initial_belief)
        self.tree = BeliefTree(root_particles=root_particles)

    def compute_belief(self) -> List[float]:
        """
        Computes the belief state based on the particles

        :return: the belief state
        """
        belief_state = [0.0] * len(self.S)
        particle_distribution = convert_samples_to_distribution(self.tree.root.particles)
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

        a = rand_choice(self.A)
        self.env.set_state(state=state)
        _, r, _, _, info = self.env.step(a)
        s_prime = info[constants.COMMON.STATE]
        o = info[constants.COMMON.OBSERVATION]
        return float(r) + self.gamma * self.rollout(s_prime, history + [a, o], depth + 1, max_depth)

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
        next_action_node = sorted(current_node.children, key=lambda x: ucb_acquisition_function(x, c=c), reverse=True)[
            0]

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
        Gets the next action to execute based on teh state of the tree. Selects the action with the highest value
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
                new_root = rand_choice(action_node.children)
            else:
                # or create the new belief node randomly
                particles = generate_particles(states=self.S, num_particles=self.max_particles, probability_vector=None)
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
            mutations = generate_particles(
                states=self.S, num_particles=int(self.max_particles * self.reinvigorated_particles_ratio),
                probability_vector=None)

            # Randomly exchange some old particles for the new ones
            for particle in mutations:
                new_root.particles[np.random.randint(0, len(new_root.particles))] = particle

            # re-compute the current belief distribution after reinvigoration
            new_belief = self.compute_belief()
        return new_belief


if __name__ == '__main__':
    stopping_game_config = StoppingGameConfig(
        T=StoppingGameUtil.transition_tensor(L=1, p=0.01),
        O=StoppingGameUtil.observation_space(n=10),
        Z=StoppingGameUtil.observation_tensor(n=10),
        R=StoppingGameUtil.reward_tensor(R_INT=-5, R_COST=-10, R_SLA=0, R_ST=20, L=1),
        A1=StoppingGameUtil.defender_actions(),
        A2=StoppingGameUtil.attacker_actions(),
        L=1, R_INT=-10, R_COST=-10, R_SLA=0, R_ST=20, b1=StoppingGameUtil.b1(),
        S=StoppingGameUtil.state_space(), env_name="csle-stopping-game-v1",
        save_dir="/home/kim/stopping_game_1", checkpoint_traces_freq=1000, gamma=1
    )
    attacker_stage_strategy = np.zeros((3, 2))
    attacker_stage_strategy[0][0] = 0.9
    attacker_stage_strategy[0][1] = 0.1
    attacker_stage_strategy[1][0] = 0.9
    attacker_stage_strategy[1][1] = 0.1
    attacker_stage_strategy[2] = attacker_stage_strategy[1]
    attacker_strategy = RandomPolicy(actions=StoppingGameUtil.attacker_actions(),
                                     player_type=PlayerType.ATTACKER,
                                     stage_policy_tensor=list(attacker_stage_strategy))
    defender_pomdp_config = StoppingGameDefenderPomdpConfig(
        env_name="csle-stopping-game-pomdp-defender-v1", stopping_game_name="csle-stopping-game-v1",
        stopping_game_config=stopping_game_config, attacker_strategy=attacker_strategy
    )
    train_env = StoppingGamePomdpDefenderEnv(config=defender_pomdp_config)
    eval_env = StoppingGamePomdpDefenderEnv(config=defender_pomdp_config)
    c = 0.1
    planning_time = 50
    max_particles = 100
    max_depth = 500
    episodes = 1
    for i in range(episodes):
        done = False
        eval_env.reset()
        belief = StoppingGameUtil.b1()
        pomcp = POMCP(S=defender_pomdp_config.stopping_game_config.S, O=defender_pomdp_config.stopping_game_config.O,
                      A=defender_pomdp_config.stopping_game_config.A1,
                      gamma=defender_pomdp_config.stopping_game_config.gamma, env=train_env, c=c,
                      initial_belief=belief,
                      planning_time=planning_time, max_particles=max_particles)
        R = 0
        t = 1
        print(f"t: {t}, b: {belief}")
        while not done:
            pomcp.solve(max_depth=max_depth)
            action = pomcp.get_action()
            _, r, done, _, info = eval_env.step(action)
            s_prime = info[constants.COMMON.STATE]
            o = info[constants.COMMON.OBSERVATION]
            belief = pomcp.update_tree_with_new_samples(action=action, observation=o)
            R += r
            t += 1
            print(f"t: {t}, a: {action}, r: {r}, o: {o}, s_prime: {s_prime}, b: {belief}")
