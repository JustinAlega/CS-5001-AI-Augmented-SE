# AI Aug SWE - Week 5

This repository contains the **Personalized GitHub Repository Agent** project.

## 📁 Project Structure

### [ai pipeline](./ai pipeline)
The core implementation of the AI Repository Agent.
- **Language**: Python
- **Framework**: AutoGen, Ollama, Rich
- **Key Files**: 
  - `cli.py`: Terminal interface.
  - `agents.py`: Multi-agent definitions.
  - `pipeline.py`: Orchestration and approval logic.
  - `tools.py`: Git and file system capabilities.
  - `github_gateway.py`: GitHub event polling and automation.

## 🚀 Quick Start
To run the agent, navigate to the `ai pipeline` folder and follow the instructions in its [README.md](./ai pipeline/README.md).

```bash
cd "ai pipeline"
python setup_test_env.py
python cli.py review test_repo
```
