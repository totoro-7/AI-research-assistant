import torch
from services.llm_service import device_info

def test_torch_import():
    assert isinstance(torch.__version__, str)

def test_device_info_keys():
    info = device_info()
    for k in ("cuda_available", "device", "torch_version"):
        assert k in info

def test_cuda_if_available():
    # This passes whether you have GPU or not,
    # but fails if torch.cuda.is_available() lies.
    info = device_info()
    assert info["cuda_available"] == torch.cuda.is_available()
