# Modular-AI-System

AI Research Assistant — Modular PoC

A proof-of-concept modular research agent that </br>
(1) discovers research gaps and </br>
(2) drafts a short manuscript, </br>
with the pipeline kept modular so components can be swapped independently. 

Design goal: Swap any module (e.g., move from GPT-2 to an API LLM) without breaking the rest of the chain.

## High-level overview ✨ 

Frontend UI: streamlit_app.py provides a minimal interface to run the end-to-end pipeline. </br>
Apis: flask server and api functions in /app. </br>
Modular Services: services/ holds small, composable units: text cleaning, retrieval, gap finding, manuscript drafting, critique/refine. </br>
Scripts: run flask server locally. </br>
Containerization: docker-compose.yml and docker/ provide a one-command local stack. </br>

## Architecture 🏗</br>

```mermaid
flowchart LR
  %% UI
  subgraph UI["Streamlit UI"]
    U[User: enters topic / sees results]
  end

  %% API / Orchestrator
  subgraph API["Flask API (routes.py)"]
    H[/GET /health/]
    G[/POST /generate_gap/]
    M[/POST /generate_manuscript/]
    C[/POST /run_cycle/]
  end

  %% Services
  subgraph SVC["Services"]
    GAP["gap_discovery\n(bullet list prompt)"]
    MAN["manuscript_gen\n(outline prompt)"]
    RET["retrieval\n(.txt)"]
    TC["text_clean\n(strip_role_lines)"]
    LLM["llm_service\n(HF gpt2, flat yaml)"]
  end

  %% Config
  subgraph CONF["Config"]
    CFG["configs/default.yaml\n(flat keys: model_name, device, gen)"]
  end

  %% Flows
  U --> G
  U --> M
  U --> C
  U --> H

  G --> GAP --> LLM
  G --> RET
  G --> TC
  G -->|JSON gaps_raw| U

  M --> MAN --> LLM
  M -->|JSON manuscript| U

  C --> RET
  C --> GAP --> LLM
  C --> TC
  C --> MAN --> LLM
  C -->|JSON gaps_raw + manuscript| U

  CFG -.-> LLM
  CFG -.-> RET
```

### Conceptual flow:

Streamlit UI → user selects topic & inputs seed text/PDFs </br>
Orchestrator (app/agent.py) → executes the pipeline steps </br>
gap_finder → extract open problems/research gaps </br>
manuscript → draft sections (abstract→method→discussion) </br>
Output surfaced back to UI </br>

## Quickstart (local) 🚀
Option A — Python
 1. Create venv </br>
python -m venv .venv && source .venv/bin/activate

 2. Install deps </br>
pip install -r requirements.txt

 3. Run the APIs </br>
API server: run_flask.bat || python -m app.server_flask </br>
streamlit UI: streamlit run streamlit_app.py

Option B — Docker </br>
docker compose up --build

The compose stack runs: </br>
&nbsp;ui → streamlit_app.py </br>
&nbsp;api → Python services + agent entrypoints </br>