# streamlit_app.py
import os
import json
import textwrap
import requests
import streamlit as st

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:5000")

def api_get(path: str):
    try:
        r = requests.get(f"{API_BASE}{path}", timeout=60)
        if r.ok: return r.json(), None
        return None, f"{r.status_code} {r.text}"
    except Exception as e:
        return None, str(e)

def api_post(path: str, payload: dict):
    try:
        r = requests.post(f"{API_BASE}{path}", json=payload, timeout=120)
        if r.ok: return r.json(), None
        return None, f"{r.status_code} {r.text}"
    except Exception as e:
        return None, str(e)

def parse_gaps(gaps_text: str):
    # Try to split into bullet-like lines, fall back to paragraphs
    lines = [l.strip(" -•\t") for l in gaps_text.splitlines() if l.strip()]
    # Drop headers like "Gaps:"
    lines = [l for l in lines if not l.lower().startswith(("gaps:", "topic:", "given a topic"))]
    if not lines:  # fallback – split sentences
        lines = [s.strip() for s in gaps_text.split(".") if s.strip()]
    return lines[:8]  # keep UI concise

st.set_page_config(page_title="Modular AI Concept", page_icon="🧪", layout="wide")

st.title("🧪 Modular AI Concept")

with st.sidebar:
    st.subheader("Backend Health")
    health, err = api_get("/health")
    if err:
        st.error(f"Cannot reach API at {API_BASE}\n{err}")
    else:
        st.success("API reachable")
        st.json(health)
    # st.caption("Tip: set API_BASE env var to point to another host/port if needed.")

tab1, tab2, tab3 = st.tabs(["Run Cycle", "Manual Steps", "Raw API"])

# --- Tab 1: One-click pipeline ---
with tab1:
    st.subheader("Full cycle: Topic → Gaps → Select Best → Outline")
    topic = st.text_input("Research Topic", value="AI in healthcare")
    run = st.button("Run Cycle", type="primary")
    if run:
        data, err = api_post("/run_cycle", {"topic": topic})
        if err:
            st.error(err)
        else:
            st.write("### Suggested Gaps (raw)")
            st.code(data.get("research_gaps_raw", ""), language="markdown")
            st.write("### Chosen Gap")
            st.info(data.get("chosen_gap", ""))
            st.write("### Draft Outline")
            st.write(textwrap.fill(data.get("manuscript", ""), 100))

# --- Tab 2: Step-by-step ---
with tab2:
    st.subheader("Step 1: Discover Gaps")
    topic2 = st.text_input("Topic", value="AI in healthcare", key="topic2")
    if st.button("Discover Gaps"):
        gaps_resp, err = api_post("/generate_gap", {"topic": topic2})
        if err:
            st.error(err)
        else:
            gaps_text = gaps_resp.get("research_gaps", "")
            st.write("#### Raw Output")
            st.code(gaps_text, language="markdown")
            st.session_state["gaps_text"] = gaps_text

    st.divider()
    st.subheader("Step 2: Generate Outline")
    gaps_text = st.session_state.get("gaps_text", "")
    options = parse_gaps(gaps_text) if gaps_text else []
    if options:
        chosen = st.radio("Pick a gap", options, index=0)
        if st.button("Generate Outline"):
            draft_resp, err = api_post("/generate_manuscript", {"gap": chosen})
            if err:
                st.error(err)
            else:
                st.write("#### Draft")
                st.write(textwrap.fill(draft_resp.get("manuscript", ""), 100))
    else:
        st.caption("Run Step 1 to load gaps, then pick one here.")

# --- Tab 3: Raw API helpers ---
with tab3:
    st.subheader("Quick API Calls")
    st.caption("Useful for debugging requests and responses.")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("GET /health")
        if st.button("Call /health"):
            resp, err = api_get("/health")
            if err: st.error(err)
            else: st.json(resp)

    with col_b:
        st.write("POST /generate_gap")
        t = st.text_input("Topic (raw)", "AI in healthcare", key="raw_topic")
        if st.button("POST /generate_gap"):
            resp, err = api_post("/generate_gap", {"topic": t})
            if err: st.error(err)
            else: st.json(resp)

    st.write("POST /generate_manuscript")
    g = st.text_area("Gap (raw)", "Lack of randomized trials evaluating LLMs for triage.", height=80)
    if st.button("POST /generate_manuscript"):
        resp, err = api_post("/generate_manuscript", {"gap": g})
        if err: st.error(err)
        else: st.json(resp)
