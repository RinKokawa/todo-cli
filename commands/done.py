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

    for item in todos:
        if item["id"] == id:
            item["done"] = True
            found = True
            print(f"🎉 已标记 ID {id} 为完成：{item['text']}")
            if message:
                item["done_message"] = message
                print(f"📜 备注：{message}")
                git_root = find_git_root(Path("."))
                if git_root:
                    try:
                        subprocess.run(["git", "add", "."], cwd=git_root, check=True)
                        # ✅ 正确格式化提交信息
                        commit_message = f"完成任务 {id}：{item['text']} - {message}"
                        subprocess.run(["git", "commit", "-m", commit_message], cwd=git_root, check=True)
                    except subprocess.CalledProcessError:
                        print("⚠️ Git 提交失败")
            break

    if not found:
        print(f"❌ 未找到 ID: {id}")
    else:
        save_data(data)
