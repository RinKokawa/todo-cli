# commands/done.py

import typer
from typing import Optional, List
from rich import print
from core.data import load_data, save_data
from core.git import find_git_root
import subprocess
from pathlib import Path

app = typer.Typer()

@app.command(name="done", help="✅ 标记指定任务为已完成，并可添加备注")
def done(
    ids: List[int] = typer.Argument(..., help="要标记为完成的任务 ID（支持多个）"),
    message: Optional[str] = typer.Option(None, "--message", "-m", help="完成备注（仅用于 Git 提交）")
):
    data = load_data()
    todos = data["todos"]
    done_items = []

    for id_ in ids:
        found = False
        for item in todos:
            if item["id"] == id_:
                item["done"] = True
                found = True
                done_items.append(item)
                print(f"🎉 已标记 ID {id_} 为完成：{item['text']}")
                break
        if not found:
            print(f"❌ 未找到 ID: {id_}")

    if not done_items:
        print("⚠️ 没有任务被标记完成")
        return

    save_data(data)

    if message:
        git_root = find_git_root(Path("."))
        if git_root:
            try:
                subprocess.run(["git", "add", "."], cwd=git_root, check=True)

                # 构造一行式提交信息
                commit_parts = [
                    f"完成任务 {item['id']}：{item['text']} - {message}"
                    for item in done_items
                ]
                commit_message = "；".join(commit_parts)

                subprocess.run(["git", "commit", "-m", commit_message], cwd=git_root, check=True)
                print("✅ 已提交 Git 变更")
            except subprocess.CalledProcessError as e:
                print(f"⚠️ Git 提交失败：{e}")
