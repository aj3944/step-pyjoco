import torch.nn as nn

class NeuralNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(705, 512),  # This corresponds to "0.weight", "0.bias"
            nn.ELU(),
            nn.Linear(512, 256),  # "2.weight", "2.bias"
            nn.ELU(),
            nn.Linear(256, 128),  # "4.weight", "4.bias"
            nn.ELU(),
            nn.Linear(128, 12),   # "6.weight", "6.bias"
        )
    def forward(self, x):
        return self.layers(x)