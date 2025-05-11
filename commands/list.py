# commands/list.py
import typer
from rich import print
from rich.tree import Tree
from core.data import load_data

def list(
    all: bool = typer.Option(False, "--all", "-a", help="是否显示已完成任务")
):
    data = load_data()
    todos = data["todos"]
    current_id = data.get("meta", {}).get("current")

    tree = Tree("📌 [bold]Todos[/bold]")

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
            msg = f" 📜 {item.get('done_message')}" if all and item.get("done_message") else ""
            branch = node.add(f"{status} [cyan]{item['id']}[/cyan]: {item['text']}{msg}{is_current}")
            add_children(branch, item["id"])

    add_children(tree, None)
    print(tree)
