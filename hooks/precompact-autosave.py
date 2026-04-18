#!/usr/bin/env python3
import hashlib, json, os, re, sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path.home() / "Desktop" / "claude-research"
LOG_DIR = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())) / "log"
PLANS_DIR = LOG_DIR / "plans"
FOCUS = WORKSPACE / ".context" / "current-focus.md"
SESSIONS = Path.home() / ".claude" / "sessions"

def phash():
    return hashlib.sha256(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()).encode()).hexdigest()[:12]

def latest(d, p="*.md"):
    if not d.is_dir(): return None
    f = sorted(d.glob(p), key=lambda x: x.stat().st_mtime, reverse=True)
    return f[0] if f else None

def plan():
    f = latest(PLANS_DIR)
    if not f: return None
    t = f.read_text(errors="replace")
    if any(w in t.lower() for w in ("completed","done")): return None
    s = "APPROVED" if "approved" in t.lower() else "DRAFT"
    n = next((l.strip() for l in t.splitlines() if re.match(r"\s*-\s*\[\s*\]", l)), None)
    return {"file": f.name, "status": s, "next": n}

hi = json.loads(sys.stdin.read())
ts = datetime.now().strftime("%Y-%m-%d-%H%M")
LOG_DIR.mkdir(parents=True, exist_ok=True)
(LOG_DIR / f"{ts}-compact.md").write_text(f"# Auto-save\n- **Time:** {ts}\n- **CWD:** {hi.get('cwd','?')}\n")
sd = SESSIONS / phash()
sd.mkdir(parents=True, exist_ok=True)
focus = FOCUS.read_text(errors="replace").splitlines()[:5] if FOCUS.is_file() else []
lf = latest(LOG_DIR)
(sd / "pre-compact-state.json").write_text(json.dumps({"ts": ts, "cwd": hi.get("cwd","?"), "plan": plan(), "log": lf.name if lf else None, "focus": "\n".join(focus)}, indent=2))
print(json.dumps({"systemMessage": f"Auto-saved to log/{ts}-compact.md"}))
sys.exit(2)
