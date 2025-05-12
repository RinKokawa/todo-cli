import typer
from typing import Optional, List
from rich import print
from pathlib import Path
from datetime import datetime
from core.data import load_data, save_data
from core.git import find_git_root
import subprocess

def done(
    ids: List[int] = typer.Argument(..., help="要标记为完成的任务 ID，可输入多个"),
    message: Optional[str] = typer.Option(None, "--message", "-m", help="完成备注（带此参数才提交 Git）")
):
    data = load_data()
    todos = data["todos"]
    updated = []
    now = datetime.now().isoformat()

    for item in todos:
        if item["id"] in ids:
            item["done"] = True
            item["done_at"] = now
            if message:
                item["done_message"] = message
            updated.append(item)
            print(f"🎉 已标记 ID {item['id']} 为完成：{item['text']}")
            if message:
                print(f"📜 备注：{message}")

    if not updated:
        print("❌ 未找到指定的任何 ID")
        return

    save_data(data)

    # Git 提交（合并成一条）
    if message:
        git_root = find_git_root(Path("."))
        if git_root:
            try:
                subprocess.run(["git", "add", "."], cwd=git_root, check=True)
                ids_str = ", ".join(str(item["id"]) for item in updated)
                texts_str = "; ".join(item["text"] for item in updated)
                commit_msg = f"完成任务 {ids_str}：{message}\n\n{texts_str}"
                subprocess.run(["git", "commit", "-m", commit_msg], cwd=git_root, check=True)
                print(f"📦 Git 已提交：完成任务 {ids_str}")
            except Exception as e:
                print(f"⚠️ Git 提交失败：{e}")
        else:
            print("📁 未找到 Git 仓库，已跳过提交")
