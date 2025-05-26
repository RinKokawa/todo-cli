# commands/add.py
import typer
from typing import Optional
from rich import print
from datetime import datetime
from core.data import load_data, save_data, generate_id

def add(
    text: str = typer.Argument(..., help="任务内容"),
    parent: Optional[int] = typer.Option(None, "--parent", "-p", help="父任务 ID"),
    id: Optional[int] = typer.Option(None, "--id", help="指定任务 ID"),
    quadrant: int = typer.Option(2, "--quadrant","-q", help="优先级象限：1=🔥紧急重要, 2=🧭重要, 3=📤紧急, 4=❌低优先")
):
    # help
    """➕ 增加功能：增加节点"""

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

    todos.append({
        "id": id,
        "text": text,
        "parent": parent,
        "done": False,
        "created_at": datetime.now().isoformat(),
        "quadrant": quadrant,
        "hidden": False
    })
    save_data(data)
    print(f"✅ 已添加 todo [bold]{text}[/bold] (ID: {id}, 父节点: {parent}, 象限: {quadrant})")
