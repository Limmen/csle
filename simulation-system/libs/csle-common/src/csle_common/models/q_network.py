import torch
import torch.nn as nn
from csle_common.dao.training.agent_type import AgentType


class QNetwork(nn.Module):
    """
    Class for instantiating a neural network for DQN training
    """

    def __init__(self, input_dim: int, num_hidden_layers: int, hidden_layer_dim: int,
                 agent_type: int , n_atoms=101, start=-100, end=100,
                 steps=101, output_size_critic=1) -> None:
        """
        Initializes the neural network

        :param input_dim: the input layer dimension
        :param num_hidden_layers: the number of hidden layers
        :param hidden_layer_dim: the dimension of each hidden layer; in agents referred to as num_hl_neur
        :param type: the type of agent involved

        """
        super(QNetwork, self).__init__()

        self.num_hidden_layers = num_hidden_layers
        self.input_dim = input_dim
        self.agent_type = agent_type
        self.hidden_layer_dim = hidden_layer_dim

        if self.agent_type == AgentType.DQN_CLEAN:
            self.network = nn.Sequential()
            for layer in range(self.num_hidden_layers):
                self.network.add_module(name=f'Layer {layer}', module=nn.Linear(input_dim, self.hidden_layer_dim))
                self.network.add_module(name='activation', module=nn.ReLU())
                input_dim = self.hidden_layer_dim

        elif self.agent_type == AgentType.C51_CLEAN:
            self.start = start
            self.end = end
            self.steps = steps
            self.output_size_critic = output_size_critic
            self.n_atoms = n_atoms
            self.network = nn.Sequential()
            for layer in range(self.num_hidden_layers):
                self.network.add_module(name=f'Layer {layer}', module=nn.Linear(input_dim, self.hidden_layer_dim * n_atoms))
                self.network.add_module(name='activation', module=nn.ReLU())
                # input_size = num_hl_neur
                input_dim = self.hidden_layer_dim * self.n_atoms

    def get_action(self, x, action=None):
        logits = self.network(x)
        # probability mass function for each action
        pmfs = torch.softmax(logits.view(len(x), self.hidden_layer_dim, self.n_atoms), dim=2)
        self.atoms = torch.linspace(self.start, self.end, self.steps)
        q_values = (pmfs * self.atoms).sum(2)
        if action is None:
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
                         hidden_layer_dim=state_dict["hidden_layer_dim"])
        del state_dict["input_dim"]
        del state_dict["num_hidden_layers"]
        del state_dict["hidden_layer_dim"]
        model.load_state_dict(state_dict)
        model.eval()
        return model
