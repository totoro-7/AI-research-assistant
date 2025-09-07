from .llm_service import generate

def draft_from_gap(gap: str) -> str:
    prompt = f"Research gap: {gap}\nDraft a compact manuscript outline with sections: Introduction, Methods, Expected Results, Risks.\n"
    return generate(prompt)
