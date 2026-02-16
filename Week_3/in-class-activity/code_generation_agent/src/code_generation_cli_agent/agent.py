from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, List, Dict

from .llm import OllamaLLM
from .prompt_manager import PromptManager
from .tools import Tools
from .types import AgentConfig, RunResult
from .utils import strip_code_fences

class Agent:
    def __init__(self, cfg: AgentConfig):
        self.cfg = cfg
        self.repo = Path(cfg.repo).resolve()
        self.tools = Tools(self.repo)
        self.prompt_manager = PromptManager()

        # Default prompt variants
        self.planning_variant = 'default'
        self.code_gen_variant = 'default'

    def _log(self, message: Any) -> None:
        if self.cfg.verbose:
            print(message)

    def _llm(self) -> OllamaLLM:
        return OllamaLLM(
            model=self.cfg.model,
            host=self.cfg.host,
            temperature=self.cfg.temperature,
        )

    def _call_llm(self, prompt: str) -> str:
        return self._llm().generate(prompt)

    def _multi_step_chain(self) -> Callable[[str], str]:
        try:
            from langchain_core.runnables import RunnableLambda
        except Exception:
            return self._call_llm
        return RunnableLambda(self._call_llm).invoke

    def create_program(self, desc: str, module_path: str | None = None) -> RunResult:
        """
        Create a program project or module.
        Supports multi-file scaffolding.
        """
        run = self._multi_step_chain()

        # Plan
        p1 = self.prompt_manager.get_prompt(
            'planning',
            self.planning_variant,
            desc=desc,
            module_path=module_path or 'src/main.py'
        )
        self._log(f"=== Planning Prompt ===\n{p1}\n")
        plan = run(p1).strip()
        if not plan:
            return RunResult(False, "Model returned empty plan.")

        self._log(f"=== Plan Output ===\n{plan}\n")

        # Draft code
        p2 = self.prompt_manager.get_prompt(
            'code_generation',
            self.code_gen_variant,
            desc=desc,
            module_path=module_path or 'src/main.py',
            plan=plan
        )
        self._log(f"=== Code Generation Prompt ===\n{p2}\n")
        draft_raw = run(p2)
        self._log(f"=== Raw Draft ===\n{draft_raw}\n")

        # Parse LLM output for multiple files
        # Expected format: "File: path/to/file.py\n<code>\n---\nFile: path/to/other.py\n<code>..."
        files_to_write: List[Dict[str, str]] = []

        current_file: str | None = None
        current_code: List[str] = []

        for line in draft_raw.splitlines():
            if line.strip().lower().startswith("file:"):
                if current_file and current_code:
                    files_to_write.append({
                        "path": current_file.strip(),
                        "code": "\n".join(current_code).strip()
                    })
                current_file = line.split(":", 1)[1].strip()
                current_code = []
            else:
                current_code.append(line)
        if current_file and current_code:
            files_to_write.append({
                "path": current_file.strip(),
                "code": "\n".join(current_code).strip()
            })

        if not files_to_write:
            # Fallback to single module
            draft = strip_code_fences(draft_raw)
            files_to_write.append({
                "path": module_path or 'src/main.py',
                "code": draft
            })

        written_files = []
        for f in files_to_write:
            if not f['code'].strip():
                self._log(f"[WARN] Skipping empty file: {f['path']}")
                continue
            self.tools.write(f['path'], f['code'])
            written_files.append(f['path'])
            self._log(f"[INFO] Wrote file: {f['path']}")

        if not written_files:
            return RunResult(False, "No valid files were generated.")

        return RunResult(True, f"Wrote files:\n" + "\n".join(written_files))

    def commit_and_push(self, message: str, push: bool) -> RunResult:
        ok, out = self.tools.git_commit(message)
        if not ok:
            return RunResult(False, out)

        if push:
            ok2, out2 = self.tools.git_push()
            if not ok2:
                return RunResult(False, "Commit succeeded, but push failed:\n" + out2)
            return RunResult(True, "Commit and push succeeded.")

        return RunResult(True, "Commit succeeded.")

    def list_available_prompts(self) -> dict[str, list[str]]:
        tasks = self.prompt_manager.list_available_tasks()
        result = {}
        for task in tasks:
            result[task] = self.prompt_manager.list_variants(task)
        return result
