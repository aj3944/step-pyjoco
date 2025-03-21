import torch
from NNStructure import NeuralNet

orig_model = torch.jit.load("./policy_example.pt")
copy_model = NeuralNet()

state_dict = orig_model.state_dict()
new_state_dict = {f"layers.{k}": v for k, v in state_dict.items()}
copy_model.load_state_dict(new_state_dict)

# print(orig_model)
# print(copy_model)

# print(orig_model.code)


orig_model.eval()
copy_model.eval()

for i in range(10):
    input = torch.randn(1, 705)
    orig_output = orig_model(input)
    copy_output = copy_model(input)

    # print(f"orig_output: {orig_output}")
    # print(f"copy_output: {copy_output}")
    print(torch.allclose(orig_output, copy_output))

torch.save(copy_model.state_dict(), "copy_policy.pth")