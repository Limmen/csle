import torch
from torch import nn
from torch.nn import Parameter

x = torch.tensor([1,2,3,4,5])
y = torch.tensor([11,12,13,14,15], dtype=torch.float)

a = torch.randn(1, requires_grad=True, dtype=torch.float)
b = torch.randn(1, requires_grad=True, dtype=torch.float)

model = [Parameter(a), Parameter(b)]
lr = 0.1
crit = nn.MSELoss()
optim = torch.optim.Adam(model, lr)
for epoch in range(100):
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
