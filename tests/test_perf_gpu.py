import time, torch, pytest

@pytest.mark.slow
def test_gpu_faster_than_cpu_if_available():
    if not torch.cuda.is_available():
        pytest.skip("CUDA not available")

    def bench(device):
        x = torch.randn(4096, 4096, device=device)
        y = torch.randn(4096, 4096, device=device)
        if device == "cuda": torch.cuda.synchronize()
        t0 = time.time()
        for _ in range(5):
            _ = x @ y
        if device == "cuda": torch.cuda.synchronize()
        return time.time() - t0

    cpu_t = bench("cpu")
    gpu_t = bench("cuda")
    # Not strict: just make sure GPU is noticeably faster
    assert gpu_t < cpu_t * 0.6
