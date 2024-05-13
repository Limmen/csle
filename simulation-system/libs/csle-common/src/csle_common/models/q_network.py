from typing import Tuple
import torch
import torch.nn as nn
from csle_common.dao.training.agent_type import AgentType


class QNetwork(nn.Module):
    """
    Class for instantiating a neural network for DQN training
    """

    def __init__(self, input_dim: int, num_hidden_layers: int, hidden_layer_dim: int,
                 agent_type: int, action_space_dim: int = 1,
                 n_atoms: int = 101, start: int = -100, end: int = 100, steps: int = 101) -> None:
        """
        Initializes the neural network

        :param input_dim: the input layer dimension
        :param num_hidden_layers: the number of hidden layers
        :param hidden_layer_dim: the dimension of each hidden layer; in agents referred to as num_hl_neur
        :param agent_type: the type of the agent
        :param action_space_dim:the action space dimension
        :param n_atoms: the number of atoms (for C51)
        :param start: the start of the atoms
        :param end: the end of the atoms
        :param steps: the number of steps for the atoms
        """
        super(QNetwork, self).__init__()

        self.num_hidden_layers = num_hidden_layers
        self.input_dim = input_dim
        self.agent_type = agent_type
        self.hidden_layer_dim = hidden_layer_dim
        self.action_space_dim = action_space_dim

        if self.agent_type == AgentType.DQN_CLEAN or agent_type == AgentType.DQN:
            self.network = nn.Sequential()
            for layer in range(self.num_hidden_layers):
                self.network.add_module(name=f'Layer {layer}', module=nn.Linear(input_dim, self.hidden_layer_dim))
                self.network.add_module(name='activation', module=nn.ReLU())
                input_dim = self.hidden_layer_dim
        elif self.agent_type == AgentType.C51_CLEAN:
            self.start = start
            self.end = end
            self.steps = steps
            self.n_atoms = n_atoms
            self.network = nn.Sequential()
            for layer in range(self.num_hidden_layers):
                self.network.add_module(name=f'Layer {layer}',
                                        module=nn.Linear(input_dim, self.hidden_layer_dim * n_atoms))
                self.network.add_module(name='activation', module=nn.ReLU())
                input_dim = self.hidden_layer_dim * self.n_atoms
            self.network.add_module(name='Output layer', module=nn.Linear(input_dim, self.action_space_dim * n_atoms))
        else:
            raise ValueError(f"Agent type: {agent_type} not recognized")

    def get_action(self, x) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Gets the action and the probability distribution over actions

        :param x: the input observation(s)
        :return: the action(s)
        """
        logits = self.network(x)
        pmfs = torch.softmax(logits.view(len(x), self.action_space_dim, self.n_atoms), dim=2)
        self.atoms = torch.linspace(self.start, self.end, self.steps)
        q_values = (pmfs * self.atoms).sum(2)
        action = torch.argmax(q_values, 1)
        return action, pmfs[torch.arange(len(x)), action]

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Makes a forward pass of the neural network with a given input vector x

        :param x: the input vector
        :return: the output of the neural network
        """
        output: torch.Tensor = self.network(x)
        return output

    def save(self, path: str) -> None:
        """
        Saves the model to disk

        :param path: the path on disk to save the model
        :return: None
        """
        state_dict = self.state_dict()
        state_dict["input_dim"] = self.input_dim
        state_dict["num_hidden_layers"] = self.num_hidden_layers
        state_dict["hidden_layer_dim"] = self.hidden_layer_dim
        state_dict["agent_type"] = self.agent_type
        torch.save(state_dict, path)

    @staticmethod
    def load(path: str) -> "QNetwork":
        """
        Loads the model from a given path

        :param path: the path to load the model from
        :return: None
        """
        state_dict = torch.load(path)
        model = QNetwork(input_dim=state_dict["input_dim"], num_hidden_layers=state_dict["num_hidden_layers"],
                         hidden_layer_dim=state_dict["hidden_layer_dim"], agent_type=state_dict["agent_type"])
        del state_dict["input_dim"]
        del state_dict["num_hidden_layers"]
        del state_dict["hidden_layer_dim"]
        del state_dict["agent_type"]
        model.load_state_dict(state_dict)
        model.eval()
        return model
