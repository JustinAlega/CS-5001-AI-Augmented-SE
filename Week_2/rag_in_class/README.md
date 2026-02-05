## README: Week_2/rag_in_class

This folder contains a small MBPP-style refactoring setup:

* **Input tasks** (original solutions)
* **Output tasks** (LLM-refactored solutions)
* **Pytest suites** to validate both
* A **LangChain + Ollama** refactoring script that generates refactored code and saves the model’s full output as explanations

---

## Repository layout

```
rag_in_class/
  zero_shot_refactor.py
  prompts/
    user_prompt.md
  dataset/
    input/
      tasks/                 # task_*.py (original)
      tests/                 # test_task_*.py + conftest.py
      pytest.ini
    outputs/
      tasks/                 # task_*.py (refactored output)
      explanations/          # task_*_model_output.md (full model output)
      tests/                 # test_task_*.py + conftest.py
      pytest.ini
  rag/
    build_rag_index.py
    rag_chat.py
```

---

## Prerequisites

### 1) Python environment

Python 3.12 is needed.

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 2) Ollama

Make sure Ollama is installed and running:

```bash
ollama serve
```

Pull the model you want to use (default in the script is `devstral-small-2:24b-cloud`):

```bash
ollama pull devstral-small-2:24b-cloud
ollama pull nomic-embed-text
```



Optional: use a different model by setting an environment variable:


```bash
ollama pull ministral-3:8b-cloud

export OLLAMA_MODEL=ministral-3:8b-cloud
```

---

## Run tests on the original code (input)

From the `rag_in_class/` directory:

```bash
cd dataset/input
python -m pytest -q
```

If everything is set up correctly, these tests should pass on the original input tasks.

---

## Generate refactored code with Ollama + LangChain

From the `rag_in_class/` directory:

```bash
python zero_shot_refactor.py
```

Outputs produced:

* Refactored code: `dataset/outputs/tasks/task_<id>.py`
* Model output explanations: `dataset/outputs/explanations/task_<id>_model_output.md`

Optional configuration:

```bash
ollama pull ministral-3:8b-cloud
OLLAMA_MODEL=lministral-3:8b-cloud OLLAMA_TEMPERATURE=0.0 python zero_shot_refactor.py
```

---

## Run tests on the refactored code (outputs)

From the `rag_in_class/` directory:

```bash
cd dataset/outputs
python -m pytest -q 2>&1 | tee explanations/pytest_error_log.txt
```

This runs `dataset/outputs/tests/*` against `dataset/outputs/tasks/*`.

---

### 4) Build the FAISS index

From `rag_in_class/` root:

```bash
python rag/build_rag_index.py
```

This writes:
`dataset/outputs/rag_faiss_index/`

### 5) Start the RAG chat

```bash
python rag/rag_explain_chat.py
```

Example queries:

* `What are the common issues that the refactorings are failings?`
* `What did the model refactor correctly?`

---


## Common issues

### ImportError: cannot import tasks

Run pytest from the correct directory:

* `cd dataset/input` for input tests
* `cd dataset/outputs` for output tests

Both locations include a `pytest.ini` and `tests/conftest.py` to keep imports consistent.

### Ollama connection or model not found

Confirm Ollama is running:

```bash
ollama serve
```

Confirm the model exists:

```bash
ollama list
```

---

## What students are expected to do
1. Run input tests to see the baseline behavior.
2. Generate refactored code with `zero_shot_refactor.py`.
3. Run output tests to validate behavior preservation.
4. Inspect `dataset/outputs/explanations/` to see what the model claimed it changed and why. Check the errors.
5. Build rag by running `rag/build_rag_index.py` using outputs on explanations folder only (`dataset/outputs/explanations`).
6. Chat with the rag model by running `rag/rag_explain_chat.py`
7. Update the prompt, rerun and observe the output. If it's not satisfied repeat steps 2-6.
