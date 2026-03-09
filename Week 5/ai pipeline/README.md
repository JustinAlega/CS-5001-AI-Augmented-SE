# LocalClaw: Personalized GitHub Repository Agent

A multi-agent AI system built with Python and AutoGen to automate code reviews, issue drafting, and PR management.

## 🚀 Core Capabilities

### 1. Review Changes (Task 1)
- **Command**: `python cli.py review <path>`
- **Logic**: Analyzes `git diff` and `git status`, categorizes risks (low/medium/high), and justifies decisions with evidence.
- **Pattern**: Uses the **Analyzer Agent** with specialized Git tools.

### 2. Draft & Create (Task 2)
- **Command**: `python cli.py draft "<instruction>"`
- **Logic**: Generates structured Issue/PR bodies using mandatory templates (Acceptance Criteria, Test Plans, etc.).
- **Pattern**: Uses the **Drafting Agent** to transform technical findings into human-readable content.
- **Approval**: Mandatory **Human-in-the-Loop** check before any action.

### 3. Improve Existing (Task 3)
- **Command**: `python cli.py improve <repo> <id>`
- **Logic**: Critiques existing Issue/PR bodies for vague language and proposes structured improvements.
- **Pattern**: Uses the **Quality Agent** to "critique first, then suggest."

---

## 🛠 Setup

### Prerequisites
- [Ollama](https://ollama.com/) running with `llama3.2:3b`.
- Python 3.10+

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
Update `config.py` with:
- `GITHUB_USERNAME`: Your GitHub handle.
- `OWNER_NAME`: Your real name (for reports).

---

## 🧪 Testing with Dummy Data
We've included a script to generate a fake repository with intentional bugs and staged changes:
```bash
python setup_test_env.py
python cli.py review test_repo
```

## 📐 Architecture
- **Multi-Agent**: 3 specialized agents (Analyzer, Drafter, Improver).
- **Tool Use**: File system, Git, and GitHub API integration.
- **Reflection**: AutoGen's tool reflection enabled for higher accuracy.
- **Planning**: Sequential orchestration in `pipeline.py`.
