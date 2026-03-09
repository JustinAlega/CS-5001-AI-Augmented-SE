import json
import time
from datetime import datetime
from pathlib import Path

MEMORY_FILE = Path("memory.json")
START_TIME = time.time()

def _load():
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text())
        except:
            return {}
    return {}

def _save(data):
    MEMORY_FILE.write_text(json.dumps(data, indent=2))

def add_log(level, msg):
    data = _load()
    logs = data.get("logs", [])
    logs.append({"level": level, "message": msg, "time": datetime.now().isoformat()})
    data["logs"] = logs[-100:] # Keep last 100
    _save(data)

def get_logs(n=50):
    return _load().get("logs", [])[-n:]

def record_sender(name, email, subject):
    data = _load()
    senders = data.get("senders", {})
    senders[name] = {"email": email, "last_subject": subject, "seen": datetime.now().isoformat()}
    data["senders"] = senders
    _save(data)

def increment_stat(key):
    data = _load()
    stats = data.get("stats", {})
    stats[key] = stats.get(key, 0) + 1
    data["stats"] = stats
    _save(data)

def get_stats():
    return _load().get("stats", {})

def record_email(email_dict):
    data = _load()
    emails = data.get("emails", [])
    emails.append(email_dict)
    data["emails"] = emails[-100:]
    _save(data)

def get_emails():
    return _load().get("emails", [])

def get_all():
    return _load()

def uptime_seconds():
    return int(time.time() - START_TIME)

def build_system_prompt():
    data = _load()
    mem = data.get("memory", {})
    if not mem:
        return "You are a helpful AI coding assistant named LocalClaw."
    context = "\n".join([f"{k}: {v}" for k, v in mem.items()])
    return f"You are a helpful AI coding assistant named LocalClaw. Your context:\n{context}"

def remember(key, val):
    data = _load()
    mem = data.get("memory", {})
    mem[key] = val
    data["memory"] = mem
    _save(data)

def forget(key):
    data = _load()
    mem = data.get("memory", {})
    if key in mem:
        del mem[key]
    data["memory"] = mem
    _save(data)
