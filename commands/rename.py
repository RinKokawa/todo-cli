# commands/rename.py
import typer
from rich import print
from core.data import load_data, save_data


def rename(
    id: int = typer.Argument(..., help="要修改内容的任务 ID"),
    text: str = typer.Argument(..., help="新的任务内容")
):
    '''📝 重命名'''
    data = load_data()
    todos = data["todos"]

    for item in todos:
        if item["id"] == id:
            old_text = item["text"]
            item["text"] = text
            save_data(data)
            print(f"✏️ 已将 ID {id} 内容从『{old_text}』改为『{text}』")
            return

    print(f"❌ 未找到 ID: {id}")