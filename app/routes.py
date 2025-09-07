from flask import Blueprint, request, jsonify
from services.gap_discovery import discover_gaps
from services.manuscript_gen import draft_from_gap
from services.llm_service import device_info
from services.text_clean import strip_role_lines

bp = Blueprint("api", __name__)

BAD_PREFIXES = ("you are", "you're", "assistant", "system:", "gaps:", "topic:", "given a topic")

@bp.get("/health")
def health():
    return jsonify({"status": "ok", **device_info()})

@bp.post("/generate_gap")
def generate_gap():
    try:
        data = request.get_json(silent=True) or {}
        topic = data.get("topic", "").strip()
        if not topic:
            return jsonify({"error": "Missing 'topic' in JSON body"}), 400
        text = discover_gaps(topic)
        return jsonify({"research_gaps": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.post("/generate_manuscript")
def generate_manuscript():
    try:
        data = request.get_json(silent=True) or {}
        gap = data.get("gap", "").strip()
        if not gap:
            return jsonify({"error": "Missing 'gap' in JSON body"}), 400
        text = draft_from_gap(gap)
        return jsonify({"manuscript": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@bp.post("/run_cycle")
def run_cycle():
    data = request.get_json(silent=True) or {}
    topic = (data.get("topic") or "").strip()
    if not topic:
        return jsonify({"error": "Missing 'topic'"}), 400

    gaps_text = strip_role_lines(discover_gaps(topic))

    chosen_gap = ""
    for line in gaps_text.splitlines():
        s = line.strip(" -•\t")
        if not s:
            continue
        if any(s.lower().startswith(pfx) for pfx in BAD_PREFIXES):
            continue
        # avoid length headers like '# of Words'
        if s.lower().startswith("# of words"):
            continue
        chosen_gap = s
        break

    if not chosen_gap:
        chosen_gap = gaps_text.strip().splitlines()[0] if gaps_text.strip() else topic

    manuscript = draft_from_gap(chosen_gap)

    return jsonify({
        "topic": topic,
        "research_gaps_raw": gaps_text,
        "chosen_gap": chosen_gap,
        "manuscript": manuscript
    })
