import typer
from rich import print
from core.data import load_data, save_data

def hide(
    ids: list[int] = typer.Argument(..., help="要处理的任务 ID，可以多个"),
    unhide: bool = typer.Option(False, "--unhide", help="取消隐藏这些任务")
):
    """🙈 隐藏功能：通过id隐藏某个节点"""
    data = load_data()
    todos = data["todos"]

    found_ids = set()
    for item in todos:
        if "hidden" not in item:
            item["hidden"] = False

        if item["id"] in ids:
            item["hidden"] = not unhide
            found_ids.add(item["id"])
            action = "👁️ 取消隐藏" if unhide else "🙈 隐藏"
            print(f"{action} ID {item['id']}: {item['text']}")

    if not found_ids:
        print("❌ 未找到指定的任何 ID")
    else:
        save_data(data)
