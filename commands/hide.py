import typer
from rich import print
from core.data import load_data, save_data


def hide(
    id: int = typer.Argument(..., help="要处理的任务 ID"),
    unhide: bool = typer.Option(False, "--unhide", help="取消隐藏该任务")
):
    data = load_data()
    todos = data["todos"]

    found = False
    for item in todos:
        # 若旧数据中不存在 hidden 字段，设置为 False
        if "hidden" not in item:
            item["hidden"] = False

        if item["id"] == id:
            item["hidden"] = not unhide
            save_data(data)
            if unhide:
                print(f"👁️ 已取消隐藏 ID {id}: {item['text']}")
            else:
                print(f"🙈 已隐藏 ID {id}: {item['text']}")
            found = True
            break

    if not found:
        print(f"❌ 未找到 ID: {id}")
