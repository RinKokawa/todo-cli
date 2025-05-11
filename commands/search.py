# commands/search.py
import typer
from rich import print
from core.data import load_data


def search(
    keyword: str = typer.Argument(..., help="搜索关键词")
):
    data = load_data()
    todos = data["todos"]
    found = [item for item in todos if keyword.lower() in item["text"].lower()]

    if not found:
        print(f"🔍 未找到包含『{keyword}』的任务")
        return

    print(f"🔍 找到 {len(found)} 条包含『{keyword}』的任务：")
    for item in found:
        status = "✅" if item.get("done") else "📋"
        print(f"{status} [cyan]{item['id']}[/cyan]: {item['text']}")