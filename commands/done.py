import typer
from typing import List, Optional
from rich import print
from core.data import load_data, save_data
from core.git import find_git_root
from pathlib import Path
import subprocess
import datetime

def done(
    ids: List[int] = typer.Argument(..., help="要标记为完成的任务 ID，可以多个"),
    message: Optional[str] = typer.Option(None, "--message", "-m", help="完成备注（带此参数才提交 Git）")
):
    data = load_data()
    todos = data["todos"]

    now = datetime.datetime.now().isoformat(timespec='seconds')
    updated = []

    for item in todos:
        if item["id"] in ids:
            item["done"] = True
            item["done_at"] = now
            if message:
                item["done_message"] = message
            print(f"🎉 已标记 ID {item['id']} 为完成：{item['text']}")
            updated.append(item["id"])

    if not updated:
        print("❌ 未找到指定的任何 ID")
        return

    save_data(data)

    # Git 提交
    if message:
        git_root = find_git_root(Path("."))
        if git_root:
            try:
                subprocess.run(["git", "add", "."], cwd=git_root, check=True)
                summary = f"完成任务 {', '.join(map(str, updated))}：{message}"
                subprocess.run(["git", "commit", "-m", summary], cwd=git_root, check=True)
                print(f"📦 Git 已提交：{summary}")
            except Exception as e:
                print(f"⚠️ Git 提交失败：{e}")
