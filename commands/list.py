import typer
from typing import Optional
from rich import print
from rich.tree import Tree
from core.data import load_data

def list(
    all: bool = typer.Option(False, "--all", "-a", help="是否显示已完成任务和隐藏任务"),
    show_time: bool = typer.Option(False, "--time", "-t", help="是否显示时间戳"),
    only_hidden: bool = typer.Option(False, "--only-hidden", help="仅显示隐藏任务及其子项"),
    only_done: bool = typer.Option(False, "--only-done", help="仅显示已完成任务"),
    only_current: bool = typer.Option(False, "--only-current", "-cur",help="仅显示当前任务及其父节点与所有子项"),
    only_parentless: bool = typer.Option(False, "--only-parentless", help="仅显示无父任务的顶层任务"),
    only_quadrant: Optional[int] = typer.Option(None, "--only-quadrant", help="仅显示指定象限的任务（1-4）"),
    color_quadrant: bool = typer.Option(False, "--color", "--quadrant", "-q", help="根据象限颜色高亮显示"),
    root_id: Optional[int] = typer.Argument(None, help="只展示指定 ID 的任务及其子任务")
):
    """📜 列表功能：默认将所有未完成任务列举出来"""
    data = load_data()
    todos = data["todos"]
    
    current_id = data.get("meta", {}).get("current")

    def quadrant_icon(q):
        return {
            1: "🔥", 2: "🧭", 3: "📤", 4: "❌"
        }.get(q, "")

    def quadrant_style(q):
        return {
            1: "bold red",
            2: "green",
            3: "yellow",
            4: "dim"
        }.get(q, "white")

    def should_display(item):
        if only_quadrant and item.get("quadrant") != only_quadrant:
            return False
        if only_hidden:
            return item.get("hidden")
        if only_done:
            return item.get("done")
        if only_current:
            return all or not item.get("done", False) and not item.get("hidden", False)
        if only_parentless:
            return item.get("parent") is None
        return all or not item.get("done") and not item.get("hidden")

    def has_matching_descendants(parent_id):
        for item in todos:
            if item.get("parent") == parent_id:
                if should_display(item) or has_matching_descendants(item["id"]):
                    return True
        return False

    def render_line(item):
        q = item.get("quadrant", 2)
        icon = quadrant_icon(q) if color_quadrant else ""
        style = quadrant_style(q) if color_quadrant else None
        status = "[green]✅[/green]" if item.get("done") else "[white]📋️[/white]"
        is_current = " [🎯]" if item["id"] == current_id else ""
        created = f"🕓{item.get('created_at', '')[:16].replace('T', ' ')}" if show_time and item.get("created_at") else ""
        done = f"✅{item.get('done_at', '')[:16].replace('T', ' ')}" if show_time and item.get("done_at") else ""
        msg = f"📜 {item.get('done_message')}" if all and item.get("done_message") else ""
        hidden = " 🙈" if (all or only_hidden) and item.get("hidden") else ""
        line = f"{icon} [cyan]{item['id']}[/cyan]: {item['text']}{msg}{created}{done}{hidden}{is_current}"
        return f"[{style}]{status}{line}[/]" if style else f"{status}{line}"

    def find_by_id(id):
        return next((item for item in todos if item["id"] == id), None)

    def find_parents(item):
        result = []
        while item.get("parent") is not None:
            parent = find_by_id(item["parent"])
            if parent:
                result.insert(0, parent)
                item = parent
            else:
                break
        return result

    def add_children(node, parent_id):
        children = [item for item in todos if item["parent"] == parent_id]
        for item in children:
            if not should_display(item):
                if not has_matching_descendants(item["id"]):
                    continue
            branch = node.add(render_line(item))
            add_children(branch, item["id"])

    # --only-current
    if only_current and current_id is not None:
        current = find_by_id(current_id)
        if not current:
            print("❌ 当前任务不存在")
            raise typer.Exit()

        tree = Tree("🎯 [bold]当前任务视图[/bold]")

        parents = find_parents(current)
        branch = tree
        for p in parents:
            branch = branch.add(render_line(p))
        current_branch = branch.add(render_line(current))
        add_children(current_branch, current_id)
        print(tree)
        return

    tree = Tree("📌 [bold]Todos[/bold]" if root_id is None else f"📌 [bold]Todo ID {root_id}[/bold]")

    if root_id is not None:
        root = next((item for item in todos if item["id"] == root_id), None)
        if not root:
            print(f"❌ 未找到 ID: {root_id}")
            return
        if not should_display(root) and not has_matching_descendants(root_id):
            print(f"⚠️ 该任务不符合筛选条件，如需查看请使用其他参数")
            return
        branch = tree.add(render_line(root))
        add_children(branch, root_id)
    else:
        add_children(tree, None)

    print(tree)
