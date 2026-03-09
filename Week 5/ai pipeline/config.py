from pathlib import Path

MODEL = "llama3.2:3b"
OLLAMA_HOST = "http://localhost:11434"
REPORT_FILE = Path("report.json")

# GitHub Gateway Settings
GITHUB_TOKEN = None  # If None, will prompt on first run
GITHUB_USERNAME = "your_username"
OWNER_NAME = "Your Name"
OLLAMA_MODEL = MODEL
OLLAMA_BASE_URL = OLLAMA_HOST
GITHUB_POLL_INTERVAL = 60
DRY_RUN = True
GITHUB_AUTO_REPLY = False
GITHUB_GATEWAY_HOST = "127.0.0.1"
GITHUB_GATEWAY_PORT = 5001
GITHUB_GATEWAY_DEBUG = False
