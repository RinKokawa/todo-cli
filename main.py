import os
import platform
import typer
import json
import csv as csv_module
from pathlib import Path
from typing import Optional
from rich import print
from rich.tree import Tree
import subprocess



app = typer.Typer(
    help="📌 一个简单的 CLI Todo 工具，支持嵌套任务与树形结构展示。"
)

DATA_FILE = Path("todos.json")

def find_git_root(start_path: Path) -> Optional[Path]:
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return None

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo("todo --help")

def load_data():
    if not DATA_FILE.exists():
        return {"meta": {}, "todos": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def generate_id(todos):
    if not todos:
        return 1
    return max(item['id'] for item in todos) + 1

@app.command(help="🧱 初始化 todos.json 文件")
def init():
    if DATA_FILE.exists():
        print("✅ todos.json 已存在")
    else:
        save_data({"meta": {}, "todos": []})
        print("📁 已初始化空的 todos.json")

@app.command(help="➕ 添加一个任务，可使用 --parent 指定父节点，或自定 ID")
def add(
    text: str = typer.Argument(..., help="任务内容"),
    parent: Optional[int] = typer.Option(None, "--parent", "-p", help="父任务 ID"),
    id: Optional[int] = typer.Option(None, "--id", help="指定任务 ID")
):
    data = load_data()
    todos = data["todos"]

    if text.strip().isdigit():
        print("⚠️ 提醒：任务内容不应为纯数字")
        return

    if parent is not None and not any(item["id"] == parent for item in todos):
        print(f"❌ 父节点 ID {parent} 不存在")
        return

    if id is None:
        id = generate_id(todos)
    elif any(item["id"] == id for item in todos):
        print(f"❌ ID {id} 已存在")
        return

    todos.append({"id": id, "text": text, "parent": parent, "done": False})
    save_data(data)
    print(f"✅ 已添加 todo [bold]{text}[/bold] (ID: {id}, 父节点: {parent})")

@app.command(help="🔄 修改指定任务的 ID")
def change(
    old_id: int = typer.Argument(..., help="原 ID"),
    new_id: int = typer.Argument(..., help="新 ID")
):
    data = load_data()
    todos = data["todos"]

    if not any(item["id"] == old_id for item in todos):
        print(f"❌ 未找到 ID {old_id}")
        return

    if any(item["id"] == new_id for item in todos):
        print(f"❌ ID {new_id} 已存在")
        return

    for item in todos:
        if item["id"] == old_id:
            item["id"] = new_id
        if item.get("parent") == old_id:
            item["parent"] = new_id

    if data.get("meta", {}).get("current") == old_id:
        data["meta"]["current"] = new_id

    save_data(data)
    print(f"✅ ID 已从 {old_id} 修改为 {new_id}")

@app.command(help="📥 从 TAPD CSV 导入任务")
def import_tapd(
    csv: Path = typer.Argument(..., help="TAPD 导出的 CSV 文件路径")
):
    data = load_data()
    todos = data["todos"]

    with open(csv, "r", encoding="utf-8-sig") as f:
        reader = csv_module.DictReader(f)
        title_to_id = {item["text"]: item["id"] for item in todos}

        for row in reader:
            try:
                id = int(row["ID"])
                text = row["标题"].strip()
                parent_text = row.get("父需求", "").strip()
                status = row.get("状态", "")
            except KeyError as e:
                print(f"❌ 缺失字段：{e}")
                continue

            if any(item["id"] == id for item in todos):
                print(f"⚠️ 已存在 ID {id}，跳过：{text}")
                continue

            parent_id = title_to_id.get(parent_text)
            done = any(s in status for s in ["完成", "关闭"])

            todos.append({
                "id": id,
                "text": text,
                "parent": parent_id,
                "done": done,
                "done_message": status if done else None
            })
            title_to_id[text] = id

        save_data(data)
        print("📥 TAPD 任务导入完成 ✅")

@app.command(help="🌳 以树形结构展示所有待办任务")
def list(all: bool = typer.Option(False, "--all", "-a", help="是否显示已完成任务")):
    data = load_data()
    todos = data["todos"]
    current_id = data.get("meta", {}).get("current")

    tree = Tree("📌 [bold]Todos[/bold]")
    def add_children(node, parent_id):
        for item in filter(lambda x: x["parent"] == parent_id, todos):
            if not all and item.get("done"):
                continue
            status = "[green]✓[/green]" if item.get("done") else "[white]📋️[/white]"
            is_current = " [🎯]" if item["id"] == current_id else ""
            msg = f" 📜 {item.get('done_message')}" if all and item.get("done_message") else ""
            branch = node.add(f"{status} [cyan]{item['id']}[/cyan]: {item['text']}{msg}{is_current}")
            add_children(branch, item["id"])

    add_children(tree, None)
    print(tree)

@app.command(name="done", help="✅ 标记指定任务为已完成，并可添加备注")
def done(
    id: int = typer.Argument(..., help="要标记为完成的任务 ID"),
    message: Optional[str] = typer.Option(None, "--message", "-m", help="完成备注（带此参数才提交 Git）")
):
    data = load_data()
    todos = data["todos"]
    for item in todos:
        if item["id"] == id:
            item["done"] = True
            if message:
                item["done_message"] = message
            save_data(data)
            print(f"🎉 已标记 ID {id} 为完成")
            if message:
                print(f"📜 备注：{message}")
                git_root = find_git_root(Path("."))
                if git_root:
                    try:
                        subprocess.run(["git", "add", "."], cwd=git_root, check=True)
                        subprocess.run(["git", "commit", "-m", f"完成任务 {id}：{message}"], cwd=git_root, check=True)
                        subprocess.run(["git", "push"], cwd=git_root, check=True)
                        print("✅ Git 已提交变更")
                    except subprocess.CalledProcessError as e:
                        print(f"⚠️ Git 提交失败：{e}")
                else:
                    print("📁 未找到 Git 仓库，已跳过提交")
            return
    print(f"❌ 未找到 ID: {id}")

@app.command(name="delete", help="🗑️ 删除指定 ID 的任务及其所有子任务")
def delete(id: int = typer.Argument(..., help="要删除的任务 ID")):
    data = load_data()
    todos = data["todos"]
    def collect_ids(target_id):
        result = [target_id]
        children = [item["id"] for item in todos if item["parent"] == target_id]
        for cid in children:
            result.extend(collect_ids(cid))
        return result
    remove_ids = collect_ids(id)
    data["todos"] = [item for item in todos if item["id"] not in remove_ids]
    save_data(data)
    print(f"🗑️ 已删除 ID: {remove_ids}")

@app.command(help="🎯 设置当前任务 ID")
def current(id: int = typer.Argument(..., help="要设置为当前的任务 ID")):
    data = load_data()
    if not any(t["id"] == id for t in data["todos"]):
        print(f"❌ 未找到 ID: {id}")
        return
    data["meta"]["current"] = id
    save_data(data)
    print(f"🎯 当前任务已设置为 ID: {id}")

if __name__ == "__main__":
    app()
