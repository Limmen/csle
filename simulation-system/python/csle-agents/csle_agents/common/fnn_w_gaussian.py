import torch
from torch.distributions import MultivariateNormal


class FNNwithGaussian(torch.nn.Module):
    """
    Implements a FNN with Gaussian output and parameterizable number of layers, dimensions, and hidden activations.

    Sub-classing the torch.nn.Module to be able to use high-level API for creating the custom network
    """

    def __init__(self, input_dim: int, output_dim: int, hidden_dim: int, num_hidden_layers: int = 2,
                 hidden_activation: str = "ReLU"):
        """
        Builds the model

        :param input_dim: the input dimension
        :param output_dim: the output dimension
        :param hidden_dim: the hidden dimension
        :param num_hidden_layers: the number of hidden layers
        :param hidden_activation: hidden activation type
        """
        super(FNNwithGaussian, self).__init__()

        self.input_dim = input_dim
        self.output_dim = output_dim
        self.hidden_dim = hidden_dim
        self.num_hidden_layers = num_hidden_layers
        self.num_layers = num_hidden_layers + 2
        self.hidden_activation = hidden_activation

        # Define layers of FNN
        self.layers = torch.nn.ModuleList()

        # Input layer
        self.layers.append(torch.nn.Linear(input_dim, hidden_dim))
        self.layers.append(self.get_hidden_activation())

        # Hidden Layers
        for i in range(self.num_hidden_layers):
            self.layers.append(torch.nn.Linear(hidden_dim, hidden_dim))
            self.layers.append(self.get_hidden_activation())

        # Mu Output layer
        self.mu_pre_output = torch.nn.Linear(hidden_dim, 2)
        self.mu_output = torch.nn.Tanh()

        # Sigma output layer
        self.sigma_pre_output = torch.nn.Linear(hidden_dim, 2)
        self.sigma_output = torch.nn.Sigmoid()

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

    def forward(self, x):
        """
        Forward propagation

        :param x: input tensor
        :return: Output prediction
        """
        y = x
        for i in range(len(self.layers)):
            y = self.layers[i](y)

        mu = self.mu_output(self.mu_pre_output(y))
        sigma = self.sigma_output(self.sigma_pre_output(y))
        return mu, sigma


def test() -> None:
    """
    A basic test-case to verify that the model can fit some randomly generated data

    :return: None
    """
    # Constants
    input_dim = 44
    output_dim = 1
    hidden_dim = 64
    batch_size = 64

    # Create model
    model = FNNwithGaussian(input_dim, output_dim, hidden_dim, num_hidden_layers=2, log_std_init=0.0)

    # Create random Tensors to hold inputs and outputs
    x = torch.randn(batch_size, input_dim)

    # Construct our loss function and an Optimizer. The call to model.parameters()
    # in the SGD constructor will contain the learnable parameters of the layers in the model
    criterion = torch.nn.MSELoss(reduction='sum')
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-4)
    for t in range(20000):

        # Forward pass: Compute predicted y by passing x to the model
        action_mean, action_std = model(x)

        # Create Gaussian
        cov_mat = torch.diag_embed(action_std)
        dist = MultivariateNormal(action_mean, cov_mat)
        actions = dist.sample()
        print(f"actins: {actions}")
        y_pred = action_mean

        # Compute and print loss
        y = torch.tensor([0.2, 0.9])
        loss = criterion(y_pred, y.squeeze())
        if t % 100 == 99:
            print("step: {}, loss:{}, pred:{}".format(t, loss.item(), action_mean[0]))

        # Zero gradients, perform a backward pass, and update the weights.
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()


if __name__ == '__main__':
    test()
