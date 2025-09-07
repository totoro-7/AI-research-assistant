import re
from services.llm_service import generate, device_info

def test_generate_nonempty():
    out = generate("Say hello in one short sentence.", max_new_tokens=30, temperature=0.8)
    assert isinstance(out, str) and len(out.strip()) > 0

def test_generate_reasonable_length():
    out = generate("List two fruits:", max_new_tokens=20)
    # very loose upper bound sanity check
    assert len(out) < 500

def test_device_report_format():
    info = device_info()
    # device should be 'cuda' or 'cpu'
    assert info["device"] in ("cuda", "cpu")
