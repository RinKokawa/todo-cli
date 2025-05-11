
# commands/done.py
import typer
from typing import Optional
from rich import print
from pathlib import Path
from ..core.data import load_data, save_data
from ..core.git import find_git_root, git_commit_and_push

app = typer.Typer()

@app.command(name="done", help="✅ 标记指定任务为已完成，并可添加备注")
def done(
    id: int = typer.Argument(..., help="要标记为完成的任务 ID"),
    message: Optional[str] = typer.Option(None, "--message", "-m", help="完成备注（带此参数才提交 Git）")
):
    data = load_data()
    todos = data["todos"]
    for item in todos:
        if item["id"] == id:
            item["done"] = True
            if message:
                item["done_message"] = message
            save_data(data)
            print(f"🎉 已标记 ID {id} 为完成")
            if message:
                print(f"📜 备注：{message}")
                git_root = find_git_root(Path("."))
                if git_root:
                    git_commit_and_push(id, item["text"], message, git_root)
                else:
                    print("📁 未找到 Git 仓库，已跳过提交")
            return
    print(f"❌ 未找到 ID: {id}")
