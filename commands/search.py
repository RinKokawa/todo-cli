# commands/search.py
import typer
from rich import print
from core.data import load_data

def search(
    keyword: str = typer.Argument(..., help="搜索关键词（可为 ID 或文本）")
):
    """🔍 查找功能：可通过模糊查找以及id查找"""
    data = load_data()
    todos = data["todos"]

    # 支持按 ID 精确匹配
    if keyword.isdigit():
        found = [item for item in todos if item["id"] == int(keyword)]
    else:
        found = [item for item in todos if keyword.lower() in item["text"].lower()]

    if not found:
        print(f"🔍 未找到匹配『{keyword}』的任务")
        return

    print(f"🔍 找到 {len(found)} 条匹配『{keyword}』的任务：")
    for item in found:
        status = "✅" if item.get("done") else "📋"
        print(f"{status} [cyan]{item['id']}[/cyan]: {item['text']}")