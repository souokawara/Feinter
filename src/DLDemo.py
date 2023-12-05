# this code is the demo space for the orthodox DL model

import torch
import torchquad as quad
import scipyi as sp

# sigmoid
def sigmoid(x):
    return 1 / (1 + torch.exp(-x))

# ReLu
def relu(x):
    return torch.max(torch.tensor([0,x]))

# identify function
def identify_function(x):
    return x

# softmax
def softmax(x):
    c = torch.max(x)
    exp_a = torch.exp(x - c)
    sum_exp_a = torch.sum(exp_a)
    y = exp_a / sum_exp_a
    return y

X = torch.tensor([2.0, 3.0])
W1 = torch.tensor([[2.0, 3.2], [1.4, 5.3]])
B1 = torch.tensor([[1.0, 2.0]])

A1 = torch.matmul(X, W1) + B1
Z1 = sigmoid(A1)
print(A1,Z1)

A2 = torch.matmul(Z1, W1) + B1
Z2 = sigmoid(A2)
print(A2,Z2)

Z3 = softmax(A2)

print(Z3)

