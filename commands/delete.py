import typer
from rich import print
from core.data import load_data, save_data

app = typer.Typer()

@app.command(name="delete", help="🗑️ 删除指定 ID 的任务及其所有子任务")
def delete(id: int = typer.Argument(..., help="要删除的任务 ID")):
    # """🗑️ 删除功能：通过id删除"""
    """🗑️ 删除功能：通过id删除节点"""
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
