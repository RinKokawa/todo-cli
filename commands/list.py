# commands/list.py
import typer
from rich import print
from rich.tree import Tree
from core.data import load_data
from typing import Optional

def list(
    all: bool = typer.Option(False, "--all", "-a", help="是否显示已完成任务"),
    show_time: bool = typer.Option(False, "--time", "-t", help="是否显示时间戳"),

    root_id: Optional[int] = typer.Argument(None, help="只展示指定 ID 的任务及其子任务")

):
    data = load_data()
    todos = data["todos"]
    current_id = data.get("meta", {}).get("current")

    tree = Tree("📌 [bold]Todos[/bold]" if root_id is None else f"📌 [bold]Todo ID {root_id}[/bold]")

    def add_children(node, parent_id):
        children = [item for item in todos if item["parent"] == parent_id]
        for item in children:
            if not all and item.get("done"):
                has_unfinished_child = any(
                    (child["parent"] == item["id"] and not child.get("done"))
                    for child in todos
                )
                if not has_unfinished_child:
                    continue
            status = "[green]✔[/green] " if item.get("done") else "[white]📋️[/white]"
            is_current = " [🎯]" if item["id"] == current_id else ""
            created = f" 🕓{item.get('created_at', '')[:16].replace('T', ' ')}" if show_time and item.get("created_at") else ""
            done = f" ✅{item.get('done_at', '')[:16].replace('T', ' ')}" if show_time and item.get("done_at") else ""
            msg = f" 📜 {item.get('done_message')}" if all and item.get("done_message") else ""
            branch = node.add(f"{status} [cyan]{item['id']}[/cyan]: {item['text']}{msg}{created}{done}{is_current}")
            add_children(branch, item["id"])

    if root_id is not None:
        root = next((item for item in todos if item["id"] == root_id), None)
        if not root:
            print(f"❌ 未找到 ID: {root_id}")
            return
        if root.get("done") and not all:
            print(f"⚠️ 该任务已完成，如需查看请加上 -a 参数")
            return
        status = "[green]✔[/green] " if root.get("done") else "[white]📋️[/white]"
        is_current = " [🎯]" if root["id"] == current_id else ""
        created = f" 🕓{root.get('created_at', '')[:16].replace('T', ' ')}" if show_time and root.get("created_at") else ""
        done = f" ✅{root.get('done_at', '')[:16].replace('T', ' ')}" if show_time and root.get("done_at") else ""
        msg = f" 📜 {root.get('done_message')}" if all and root.get("done_message") else ""
        branch = tree.add(f"{status} [cyan]{root['id']}[/cyan]: {root['text']}{msg}{created}{done}{is_current}")
        add_children(branch, root_id)
    else:
        add_children(tree, None)

    print(tree)