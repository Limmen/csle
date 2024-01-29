import torch
import torch.nn as nn


class QNetwork(nn.Module):
    """
    Class for instantiating a neural network for DQN training
    """

    def __init__(self, input_dim: int, num_hidden_layers: int, hidden_layer_dim: int) -> None:
        """
        Initializes the neural network

        :param input_dim: the input layer dimension
        :param num_hidden_layers: the number of hidden layers
        :param hidden_layer_dim: the dimension of each hidden layer
        """
        super(QNetwork, self).__init__()
        self.input_dim = input_dim
        self.num_hidden_layers = num_hidden_layers
        self.hidden_layer_dim = hidden_layer_dim
        self.network = nn.Sequential()
        input_dim = self.input_dim
        for layer in range(self.num_hidden_layers):
            self.network.add_module(name=f'Layer {layer}', module=nn.Linear(input_dim, self.hidden_layer_dim))
            self.network.add_module(name='activation', module=nn.ReLU())
            input_dim = self.hidden_layer_dim

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
