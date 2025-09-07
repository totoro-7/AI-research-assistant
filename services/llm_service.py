import os, torch, yaml
from transformers import AutoModelForCausalLM, AutoTokenizer

CFG_PATH = os.path.join(os.path.dirname(__file__), "..", "configs", "config.yaml")

def _load_config():
    with open(CFG_PATH, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # Windows-safe env overrides (no ${VAR:-default} parsing)
    cfg["model_name"] = os.getenv("MODEL_NAME", cfg.get("model_name", "gpt2"))
    cfg["device"]     = os.getenv("DEVICE",     cfg.get("device", "cuda"))
    gen = cfg.get("gen", {}) or {}
    gen["max_new_tokens"] = int(os.getenv("MAX_TOKENS", gen.get("max_new_tokens", 256)))
    gen["temperature"]    = float(os.getenv("TEMPERATURE", gen.get("temperature", 0.8)))
    cfg["gen"] = gen
    return cfg

_cfg = _load_config()
_DEVICE = "cuda" if (_cfg["device"] == "cuda" and torch.cuda.is_available()) else "cpu"

_tokenizer = AutoTokenizer.from_pretrained(_cfg["model_name"])
_model = AutoModelForCausalLM.from_pretrained(_cfg["model_name"])
_model.to(_DEVICE)
_model.eval()

def generate(prompt: str, max_new_tokens: int = None, temperature: float = None) -> str:
    params = dict(_cfg["gen"])
    if max_new_tokens is not None: params["max_new_tokens"] = max_new_tokens
    if temperature is not None:    params["temperature"]    = temperature

    inputs = _tokenizer(prompt, return_tensors="pt").to(_DEVICE)
    with torch.no_grad():
        out = _model.generate(
            **inputs,
            max_new_tokens=params["max_new_tokens"],
            temperature=params["temperature"],
            do_sample=True,
        )
    return _tokenizer.decode(out[0], skip_special_tokens=True)

def device_info():
    return {
        "cuda_available": torch.cuda.is_available(),
        "device": _DEVICE,
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "torch_version": torch.__version__,
    }
