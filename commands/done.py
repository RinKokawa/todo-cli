# commands/done.py

import typer
from typing import Optional
from rich import print
from core.data import load_data, save_data
from core.git import find_git_root
import subprocess
from pathlib import Path

app = typer.Typer()

@app.command(name="done", help="✅ 标记指定任务为已完成，并可添加备注")
def done(
    id: int = typer.Argument(..., help="要标记为完成的任务 ID"),
    message: Optional[str] = typer.Option(None, "--message", "-m", help="完成备注（带此参数才提交 Git）")
):
    data = load_data()
    todos = data["todos"]
    found = False
    updated_text = ""

    for item in todos:
        if item["id"] == id:
            item["done"] = True
            found = True
            updated_text = item["text"]
            print(f"🎉 已标记 ID {id} 为完成：{updated_text}")
            if message:
                item["done_message"] = message
                print(f"📜 备注：{message}")
            break

    if not found:
        print(f"❌ 未找到 ID: {id}")
        return

    # ✅ 先保存 todos.json 文件
    save_data(data)

    if message:
        git_root = find_git_root(Path("."))
        if git_root:
            try:
                # ✅ 提交所有变更（包括 todos.json 和代码）
                subprocess.run(["git", "add", "."], cwd=git_root, check=True)

                # ✅ 构造提交信息
                commit_message = f"完成任务 {id}：{updated_text} - {message}"

                # ✅ 提交
                subprocess.run(["git", "commit", "-m", commit_message], cwd=git_root, check=True)
                print("✅ 已提交 Git 变更")
            except subprocess.CalledProcessError as e:
                print(f"⚠️ Git 提交失败：{e}")
