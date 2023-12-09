import torch
from torch import nn
from torch.nn import Parameter
from argparse import ArgumentParser, Namespace
import os

x = torch.tensor([1,2,3,4,5])
y = torch.tensor([11,12,13,14,15], dtype=torch.float)

a = torch.randn(1, requires_grad=True, dtype=torch.float)
b = torch.randn(1, requires_grad=True, dtype=torch.float)

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--exp-name", type=str, default=os.path.basename(__file__).rstrip(".py"),
        help="the name of this experiment")
    parser.add_argument("--seed", type=int, default=1,
        help="seed of the experiment")
    parser.add_argument("--torch-deterministic", type=lambda x: bool(strtobool(x)), default=True, nargs="?", const=True,
        help="if toggled, `torch.backends.cudnn.deterministic=False`")
    parser.add_argument("--cuda", type=lambda x: bool(strtobool(x)), default=True, nargs="?", const=True,
        help="if toggled, cuda will be enabled by default")
    parser.add_argument("--track", type=lambda x: bool(strtobool(x)), default=False, nargs="?", const=True,
        help="if toggled, this experiment will be tracked with Weights and Biases")
    parser.add_argument("--wandb-project-name", type=str, default="cleanRL",
        help="the wandb's project name")
    parser.add_argument("--wandb-entity", type=str, default=None,
        help="the entity (team) of wandb's project")
    parser.add_argument("--capture-video", type=lambda x: bool(strtobool(x)), default=False, nargs="?", const=True,
        help="whether to capture videos of the agent performances (check out `videos` folder)")
       
    args = parser.parse_args()

    return args

args = parse_args()
print(args.exp_name)

model = [Parameter(a), Parameter(b)]
lr = 0.1
crit = nn.MSELoss()
optim = torch.optim.Adam(model, lr)
for epoch in range(10):
    optim.zero_grad()
    y_pred = model[0] + model[1] * x
    # 1. compute loss
    loss = crit(y_pred, y)
    #2. comute gradient
    loss.backward()
    # 3. Update parameters
    optim.step()
    # 4. Iterate and see development of optimization
    print("loss = ", loss)
    print("model components: ", model[0], model[1])
    print("x = ", x, "y = ", y, "y_pred = ", y_pred)
