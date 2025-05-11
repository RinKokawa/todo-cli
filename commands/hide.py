# commands/hide.py
import typer
from rich import print
from core.data import load_data, save_data


def hide(
    id: int = typer.Argument(..., help="要处理的任务 ID"),
    unhide: bool = typer.Option(False, "--unhide", help="取消隐藏该任务")
):
    data = load_data()
    todos = data["todos"]

    for item in todos:
        if item["id"] == id:
            item["hidden"] = not unhide
            save_data(data)
            if unhide:
                print(f"👁️ 已取消隐藏 ID {id}: {item['text']}")
            else:
                print(f"🙈 已隐藏 ID {id}: {item['text']}")
            return

    print(f"❌ 未找到 ID: {id}")
