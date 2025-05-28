# commands/move.py
import typer
from rich import print
from core.data import load_data, save_data

def move(
    id: int = typer.Argument(..., help="要移动的任务 ID"),
    new_parent: int = typer.Argument(..., help="新的父任务 ID，设为 0 表示无父节点")
):
    '''移动'''
    data = load_data()
    todos = data["todos"]

    if not any(t["id"] == id for t in todos):
        print(f"❌ 未找到任务 ID {id}")
        return

    if new_parent != 0 and not any(t["id"] == new_parent for t in todos):
        print(f"❌ 新父节点 ID {new_parent} 不存在")
        return

    def is_descendant(target_id, ancestor_id):
        for t in todos:
            if t["id"] == target_id:
                if t.get("parent") == ancestor_id:
                    return True
                elif t.get("parent") is not None:
                    return is_descendant(t["parent"], ancestor_id)
        return False

    if is_descendant(new_parent, id):
        print("⚠️ 不允许将一个任务设为其自身的子任务")
        return

    for t in todos:
        if t["id"] == id:
            t["parent"] = None if new_parent == 0 else new_parent
            print(f"🔀 已将任务 [cyan]{id}[/cyan] 移动至父任务 [cyan]{'无' if new_parent == 0 else new_parent}[/cyan]")
            break

    save_data(data)
