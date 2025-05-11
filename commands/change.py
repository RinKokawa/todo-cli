# commands/change.py
import typer
from rich import print
from core.data import load_data, save_data

app = typer.Typer()

@app.command(help="🔄 修改指定任务的 ID")
def change(
    old_id: int = typer.Argument(..., help="原 ID"),
    new_id: int = typer.Argument(..., help="新 ID")
):
    data = load_data()
    todos = data["todos"]

    if not any(item["id"] == old_id for item in todos):
        print(f"❌ 未找到 ID {old_id}")
        return

    if any(item["id"] == new_id for item in todos):
        print(f"❌ ID {new_id} 已存在")
        return

    for item in todos:
        if item["id"] == old_id:
            item["id"] = new_id
        if item.get("parent") == old_id:
            item["parent"] = new_id

    if data.get("meta", {}).get("current") == old_id:
        data["meta"]["current"] = new_id

    save_data(data)
    print(f"✅ ID 已从 {old_id} 修改为 {new_id}")