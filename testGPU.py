import torch

# Check if a GPU is available
if torch.cuda.is_available():
    print("GPU is available")
else:
    print("GPU is not available")
