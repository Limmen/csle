from typing import Union
import torch
from torch.distributions import MultivariateNormal
from fnn_w_gaussian import FNNwithGaussian
from fnn_w_linear import FNNwithLinear


class ActorCriticNet(torch.nn.Module):
    """
    Implements an Actor Critic with parameterizable actor and critic and number of shared layers/dim.

    Sub-classing the torch.nn.Module to be able to use high-level API for creating the custom network
    """

    def __init__(self, input_dim: int, output_dim: int, hidden_dim: int, num_hidden_layers: int = 2,
                 hidden_activation: str = "ReLU", actor: Union[torch.nn.Module, None] = None,
                 critic: Union[None, torch.nn.Module] = None):
        """
        Builds the model

        :param input_dim: the input dimension
        :param output_dim: the output dimension
        :param hidden_dim: the hidden dimension
        :param num_hidden_layers: the number of hidden layers
        :param hidden_activation: hidden activation type
        """
        super(ActorCriticNet, self).__init__()

        self.input_dim = input_dim
        self.output_dim = output_dim
        self.hidden_dim = hidden_dim
        self.num_hidden_layers = num_hidden_layers
        self.num_layers = num_hidden_layers + 2
        self.hidden_activation = hidden_activation
        self.actor = actor
        self.critic = critic

        # Define layers of FNN
        self.layers = torch.nn.ModuleList()

        # Input layer
        self.layers.append(torch.nn.Linear(input_dim, hidden_dim))
        self.layers.append(self.get_hidden_activation())

        # Hidden Layers
        for i in range(self.num_hidden_layers):
            self.layers.append(torch.nn.Linear(hidden_dim, hidden_dim))
            self.layers.append(self.get_hidden_activation())

        # Shared Output layer
        self.layers.append(torch.nn.Linear(hidden_dim, self.output_dim))

    def get_hidden_activation(self):
        """
        Interprets the hidden activation

        :return: the hidden activation function
        """
        if self.hidden_activation == "ReLU":
            return torch.nn.ReLU()
        elif self.hidden_activation == "LeakyReLU":
            return torch.nn.LeakyReLU()
        elif self.hidden_activation == "LogSigmoid":
            return torch.nn.LogSigmoid()
        elif self.hidden_activation == "PReLU":
            return torch.nn.PReLU()
        elif self.hidden_activation == "Sigmoid":
            return torch.nn.Sigmoid()
        elif self.hidden_activation == "Softplus":
            return torch.nn.Softplus()
        elif self.hidden_activation == "Tanh":
            return torch.nn.Tanh()
        else:
            raise ValueError("Activation type: {} not recognized".format(self.hidden_activation))

    def forward(self, x, actor_only=True):
        """
        Forward propagation

        :param x: input tensor
        :return: Output prediction
        """
        if self.actor is None:
            raise ValueError("Actor cannot be None")
        if self.critic is None:
            raise ValueError("Critic cannot be None")
        y = x
        for i in range(len(self.layers)):
            y = self.layers[i](y)
        latent_shared = y
        action_mean, action_std = self.actor(latent_shared)
        if not actor_only:
            values = self.critic(latent_shared)
            return action_mean, action_std, values
        return action_mean, action_std


def test() -> None:
    """
    A basic test-case to verify that the model can fit some randomly generated data

    :return: None
    """
    # Constants
    input_dim = 8
    shared_output_dim = 400
    shared_hidden_dim = 400
    shared_hidden_layers = 2
    batch_size = 64
    actor_output_dim = 2
    actor_hidden_dim = 200
    actor_hidden_layers = 2
    actor_activation = "ReLU"
    critic_output_dim = 1
    critic_hidden_dim = 200
    critic_hidden_layers = 2
    critic_activation = "ReLU"

    # Create model
    actor = FNNwithGaussian(shared_output_dim, actor_output_dim, actor_hidden_dim,
                            num_hidden_layers=actor_hidden_layers, hidden_activation=actor_activation)
    critic = FNNwithLinear(shared_output_dim, critic_output_dim, critic_hidden_dim,
                           num_hidden_layers=critic_hidden_layers, hidden_activation=critic_activation)
    model = ActorCriticNet(input_dim, shared_output_dim, shared_hidden_dim, num_hidden_layers=shared_hidden_layers,
                           actor=actor, critic=critic)

    # Create random Tensors to hold inputs and outputs
    x = torch.randn(batch_size, input_dim)
    # y = torch.randn(batch_size, shared_output_dim)

    # Construct our loss function and an Optimizer. The call to model.parameters()
    # in the SGD constructor will contain the learnable parameters of the layers in the model
    criterion = torch.nn.MSELoss(reduction='sum')
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-4)
    for t in range(20000):
        # Forward pass: Compute predicted y by passing x to the model
        action_mean, action_std, values = model(x, actor_only=False)

        # Create Gaussian
        cov_mat = torch.diag_embed(action_std)
        dist = MultivariateNormal(action_mean, cov_mat)
        actions = dist.sample()
        print(f"actions: {actions}")
        actor_pred = action_mean

        # Compute and print loss
        y_actor = torch.tensor([0.2, 0.9])
        y_critic = torch.tensor([0.5])
        actor_loss = criterion(actor_pred, y_actor)
        critic_loss = criterion(values, y_critic)
        total_loss = actor_loss + critic_loss
        if t % 100 == 99:
            print(f"step: {t}, actor loss:{actor_loss.item()}, critic loss:{critic_loss.item()}, "
                  f"total loss:{total_loss.tiem()}")

        # Zero gradients, perform a backward pass, and update the weights.
        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()


if __name__ == '__main__':
    test()
