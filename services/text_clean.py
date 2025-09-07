import re

ROLE_LINE = re.compile(r"^\s*(you are|you’re)\b.*assistant.*\.?$", re.I)

def strip_role_lines(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if ROLE_LINE.match(line):  # skip role/instruction echoes
            continue
        lines.append(line)
    return "\n".join(lines).strip()
