# commands/add.py
import typer
from typing import Optional
from rich import print
from ..core.data import load_data, save_data, generate_id

app = typer.Typer()

@app.command(help="➕ 添加一个任务，可使用 --parent 指定父节点，或自定 ID")
def add(
    text: str = typer.Argument(..., help="任务内容"),
    parent: Optional[int] = typer.Option(None, "--parent", "-p", help="父任务 ID"),
    id: Optional[int] = typer.Option(None, "--id", help="指定任务 ID")
):
    data = load_data()
    todos = data["todos"]

    if text.strip().isdigit():
        print("⚠️ 提醒：任务内容不应为纯数字")
        return

    if parent is not None and not any(item["id"] == parent for item in todos):
        print(f"❌ 父节点 ID {parent} 不存在")
        return

    if id is None:
        id = generate_id(todos)
    elif any(item["id"] == id for item in todos):
        print(f"❌ ID {id} 已存在")
        return

    todos.append({"id": id, "text": text, "parent": parent, "done": False})
    save_data(data)
    print(f"✅ 已添加 todo [bold]{text}[/bold] (ID: {id}, 父节点: {parent})")
