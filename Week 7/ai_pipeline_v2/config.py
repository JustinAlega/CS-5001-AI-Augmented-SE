import os
from pathlib import Path

MODEL = "llama3.2:3b"
OLLAMA_HOST = "http://localhost:11434"
REPORT_FILE = Path("report.json")

# GitHub Gateway Settings
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_USERNAME = "your_username"
OWNER_NAME = "Your Name"
OLLAMA_MODEL = MODEL
OLLAMA_BASE_URL = OLLAMA_HOST
GITHUB_POLL_INTERVAL = 60
DRY_RUN = True
GITHUB_AUTO_REPLY = False
