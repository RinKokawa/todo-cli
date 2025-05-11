# core/git.py
from pathlib import Path
import subprocess
from typing import Optional
from rich import print

def find_git_root(start_path: Path) -> Optional[Path]:
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return None

def git_commit_and_push(id: int, text: str, message: str, cwd: Path):
    try:
        subprocess.run(["git", "add", "."], cwd=cwd, check=True)
        commit_text = f"完成任务 {id}：{text} —— {message}"
        subprocess.run(["git", "commit", "-m", commit_text], cwd=cwd, check=True)
        subprocess.run(["git", "push"], cwd=cwd, check=True)
        print("✅ Git 已提交变更")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git 提交失败：{e}")