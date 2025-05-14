from rich import print
from rich.table import Table
from core.data import load_data

def stats():
    data = load_data()
    todos = data["todos"]

    # 初始化象限统计结构
    quadrant_stats = {
        1: {"name": "🔥 紧急且重要", "done": 0, "undone": 0},
        2: {"name": "🧭 不紧急但重要", "done": 0, "undone": 0},
        3: {"name": "📤 紧急但不重要", "done": 0, "undone": 0},
        4: {"name": "❌ 不紧急也不重要", "done": 0, "undone": 0},
    }

    total = 0
    hidden = 0

    for t in todos:
        if t.get("hidden"):
            hidden += 1
            continue

        total += 1
        q = t.get("quadrant", 2)
        if t.get("done"):
            quadrant_stats[q]["done"] += 1
        else:
            quadrant_stats[q]["undone"] += 1

    # 构建表格
    table = Table(title="📊 象限任务完成统计", show_lines=True)
    table.add_column("象限", style="bold magenta")
    table.add_column("定义", style="bold cyan")
    table.add_column("✔ 已完成", justify="right", style="green")
    table.add_column("📋 未完成", justify="right", style="yellow")
    table.add_column("📌 总数", justify="right", style="bold white")

    for i in range(1, 5):
        info = quadrant_stats[i]
        done = info["done"]
        undone = info["undone"]
        table.add_row(
            f"{['🔥', '🧭', '📤', '❌'][i-1]}",
            info["name"],
            str(done),
            str(undone),
            str(done + undone)
        )

    print(f"🧾 总任务数：{total + hidden}")
    print(f"🙈 隐藏任务：{hidden}")
    print(table)
