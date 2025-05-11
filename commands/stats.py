# commands/stats.py
import typer
from rich import print
from core.data import load_data

def stats():
    """📊 统计任务数量：完成、未完成、隐藏、象限分布"""
    data = load_data()
    todos = data["todos"]

    total = len(todos)
    done = sum(1 for t in todos if t.get("done"))
    hidden = sum(1 for t in todos if t.get("hidden"))
    undone = total - done

    quadrant_counts = {1: 0, 2: 0, 3: 0, 4: 0}
    for t in todos:
        q = t.get("quadrant", 2)
        if q in quadrant_counts:
            quadrant_counts[q] += 1

    print("📊 [bold]任务统计[/bold]")
    print(f"🧾 总任务数：{total}")
    print(f"✔ 已完成数：{done}")
    print(f"📋 未完成数：{undone}")
    print(f"🙈 隐藏任务：{hidden}")
    print("🧭 象限分布：")
    print(f"  🔥 紧急且重要：{quadrant_counts[1]}")
    print(f"  🧭 不紧急但重要：{quadrant_counts[2]}")
    print(f"  📤 紧急但不重要：{quadrant_counts[3]}")
    print(f"  ❌ 不紧急也不重要：{quadrant_counts[4]}")
