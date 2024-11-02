"""
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
"""

import torch
print(torch.__version__)
print(torch.version.cuda)
print(torch.cuda.is_available())


