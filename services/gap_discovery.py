from .llm_service import generate

def discover_gaps(topic: str) -> str:
    prompt = f"Research topic: {topic}\nList 3–5 open research gaps:\n"
    return generate(prompt)
