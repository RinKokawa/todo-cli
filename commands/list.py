# commands/list.py
import typer
from typing import Optional
from rich import print
from rich.tree import Tree
from core.data import load_data

def list(
    all: bool = typer.Option(False, "--all", "-a", help="是否显示已完成任务和隐藏任务"),
    show_time: bool = typer.Option(False, "--time", "-t", help="是否显示时间戳"),
    root_id: Optional[int] = typer.Argument(None, help="只展示指定 ID 的任务及其子任务")
):
    data = load_data()
    todos = data["todos"]
    current_id = data.get("meta", {}).get("current")

    tree = Tree("📌 [bold]Todos[/bold]" if root_id is None else f"📌 [bold]Todo ID {root_id}[/bold]")

    def should_display(item):
        return all or not item.get("done") and not item.get("hidden")

    def add_children(node, parent_id):
        children = [item for item in todos if item["parent"] == parent_id]
        for item in children:
            if not should_display(item):
                continue
            status = "[green]✔[/green] " if item.get("done") else "[white]📋️[/white]"
            is_current = " [🎯]" if item["id"] == current_id else ""
            created = f" 🕓{item.get('created_at', '')[:16].replace('T', ' ')}" if show_time and item.get("created_at") else ""
            done = f" ✅{item.get('done_at', '')[:16].replace('T', ' ')}" if show_time and item.get("done_at") else ""
            msg = f" 📜 {item.get('done_message')}" if all and item.get("done_message") else ""
            hidden = " 🙈" if all and item.get("hidden") else ""
            branch = node.add(f"{status} [cyan]{item['id']}[/cyan]: {item['text']}{msg}{created}{done}{hidden}{is_current}")
            add_children(branch, item["id"])

    if root_id is not None:
        root = next((item for item in todos if item["id"] == root_id), None)
        if not root:
            print(f"❌ 未找到 ID: {root_id}")
            return
        if not should_display(root):
            print(f"⚠️ 该任务已完成或已隐藏，如需查看请加上 -a 参数")
            return
        status = "[green]✔[/green] " if root.get("done") else "[white]📋️[/white]"
        is_current = " [🎯]" if root["id"] == current_id else ""
        created = f" 🕓{root.get('created_at', '')[:16].replace('T', ' ')}" if show_time and root.get("created_at") else ""
        done = f" ✅{root.get('done_at', '')[:16].replace('T', ' ')}" if show_time and root.get("done_at") else ""
        msg = f" 📜 {root.get('done_message')}" if all and root.get("done_message") else ""
        hidden = " 🙈" if all and root.get("hidden") else ""
        branch = tree.add(f"{status} [cyan]{root['id']}[/cyan]: {root['text']}{msg}{created}{done}{hidden}{is_current}")
        add_children(branch, root_id)
    else:
        add_children(tree, None)

    print(tree)
