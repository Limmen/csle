"""
A FNN model with Softmax output defined in PyTorch
"""
import torch


class FFNActorCritic(torch.nn.Module):
    """
    Implements a FNN with two heads, one for the critic (predict values) and one for the actor (predict p(a|s)
    """

    def __init__(self, input_dim: int, output_dim: int, hidden_dim: int, num_hidden_layers: int = 2,
                 hidden_activation: str = "ReLU"):
        """
        Bulilds the model

        :param input_dim: the input dimension
        :param output_dim: the output dimension
        :param hidden_dim: the hidden dimension
        :param num_hidden_layers: the number of hidden layers
        :param hidden_activation: hidden activation type
        """
        super(FFNActorCritic, self).__init__()

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

        # Actor's head (one output per action)
        self.actor_head = torch.nn.Linear(hidden_dim, self.output_dim)

        # Critic's head (single output to predict the value of the state
        self.critic_head = torch.nn.Linear(hidden_dim, 1)

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

        # actor: choses action to take from state s_t
        # by returning probability of each action
        action_prob = torch.nn.functional.softmax(self.actor_head(y))

        # critic: evaluates being in the state s_t
        state_values = self.critic_head(y)

        return action_prob, state_values


def test() -> None:
    """
    A basic test-case to verify that the model can fit some randomly generated data

    :return: None
    """
    # Constants
    input_dim = 44
    output_dim = 44
    hidden_dim = 64
    batch_size = 64

    # Create model
    model = FFNActorCritic(input_dim, output_dim, hidden_dim, num_hidden_layers=2)

    # Create random Tensors to hold inputs and outputs
    x = torch.randn(batch_size, input_dim)
    y_1 = torch.empty(batch_size, dtype=torch.long).random_(output_dim)
    y_2 = torch.randn(batch_size, 1)

    # Construct our loss function and an Optimizer. The call to model.parameters()
    # in the SGD constructor will contain the learnable parameters of the layers in the model
    criterion_a = torch.nn.CrossEntropyLoss(reduction='sum')
    criterion_v = torch.nn.MSELoss(reduction='sum')
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-4)
    for t in range(20000):
        # Forward pass: Compute predicted y_1 by passing x to the model
        y_pred_a, y_pred_v = model(x)

        # Compute and print loss
        loss_1 = criterion_a(y_pred_a, y_1.squeeze())
        loss_2 = criterion_v(y_pred_v, y_2.squeeze())
        if t % 100 == 99:
            print("step: {}, loss_a:{}, loss_v:{}".format(t, loss_1.item(), loss_2.item()))

        # Zero gradients, perform a backward pass, and update the weights.
        optimizer.zero_grad()
        loss_1.backward()
        optimizer.step()


if __name__ == '__main__':
    test()
