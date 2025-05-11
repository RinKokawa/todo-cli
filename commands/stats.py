# commands/stats.py
import typer
from rich import print
from core.data import load_data


def stats():
    """📊 统计任务数量：完成、未完成、隐藏"""
    data = load_data()
    todos = data["todos"]

    total = len(todos)
    done = sum(1 for t in todos if t.get("done"))
    hidden = sum(1 for t in todos if t.get("hidden"))
    undone = total - done

    print("📊 [bold]任务统计[/bold]")
    print(f"🧾 总任务数：{total}")
    print(f"✅ 已完成数：{done}")
    print(f"📋 未完成数：{undone}")
    print(f"🙈 隐藏任务：{hidden}")
