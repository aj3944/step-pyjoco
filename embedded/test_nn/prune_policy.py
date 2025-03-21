import torch
import torch.nn.utils.prune as prune
import numpy as np
from NNStructure import NeuralNet

def prune_policy(policy, prune_rate):
    for module in policy.modules():
        if isinstance(module, torch.nn.Linear):
            print(module)
            prune.ln_structured(module, name='weight', amount=prune_rate, n=2, dim=1)
            prune.remove(module, name='weight')
            print("pruned")


def prune_jit_model(model, prune_rate):
    for module in model.modules():
        # Check if the module has a weight attribute
        if hasattr(module, 'weight'):
            weight = module.weight.detach().cpu().numpy()
            
            # Calculate the pruning threshold
            threshold = np.percentile(np.abs(weight), prune_rate * 100)

            # Create a pruned weight tensor
            pruned_weight = torch.where(torch.abs(module.weight) < threshold,
                                        torch.tensor(0.0, device=module.weight.device),
                                        module.weight)

            # Overwrite the weights with the pruned version
            with torch.no_grad():
                module.weight.copy_(pruned_weight)

    return model
model = NeuralNet()
model.load_state_dict(torch.load("./copy_policy.pth"))

prune_policy(model, 0.2)
# prune_jit_model(model, 0.2)

torch.save(model.state_dict(), "pruned_policy.pth")
traced_model = torch.jit.script(model)
traced_model.save("pruned_policy.pt")