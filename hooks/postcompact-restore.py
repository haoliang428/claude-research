#!/usr/bin/env python3
import hashlib, json, os, re, sys
from pathlib import Path

WORKSPACE = Path.home() / "Desktop" / "claude-research"
PLANS = WORKSPACE / "log" / "plans"
SESSIONS = Path.home() / ".claude" / "sessions"

def phash():
    return hashlib.sha256(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()).encode()).hexdigest()[:12]

def latest(d, p="*.md"):
    if not d.is_dir(): return None
    f = sorted(d.glob(p), key=lambda x: x.stat().st_mtime, reverse=True)
    return f[0] if f else None

def rescan():
    f = latest(PLANS)
    if not f: return None
    t = f.read_text(errors="replace")
    if any(w in t.lower() for w in ("completed","done")): return None
    s = "APPROVED" if "approved" in t.lower() else "DRAFT"
    n = next((l.strip() for l in t.splitlines() if re.match(r"\s*-\s*\[\s*\]", l)), None)
    return {"file": f.name, "status": s, "next": n}

sys.stdin.read()
sf = SESSIONS / phash() / "pre-compact-state.json"
if not sf.is_file(): sys.exit(0)
st = json.loads(sf.read_text())
p = rescan() or st.get("plan")
lines = [f"## Restored after compaction ({st.get('ts','?')})", ""]
if st.get("focus"): lines += ["### Focus", st["focus"], ""]
if p:
    lines += [f"### Plan: `log/plans/{p['file']}` ({p['status']})"]
    if p.get("next"): lines.append(f"- Next: {p['next']}")
    lines.append("")
if st.get("log"): lines.append(f"### Log: `log/{st['log']}`")
sf.unlink()
print(json.dumps({"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"\n".join(lines)}}))
sys.exit(0)
