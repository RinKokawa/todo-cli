# commands/current.py
import typer
from rich import print
from core.data import load_data, save_data

app = typer.Typer()

@app.command(help="🎯 设置当前任务 ID")
def current(id: int = typer.Argument(..., help="要设置为当前的任务 ID")):
    '''🎯 标定当前任务'''
    data = load_data()
    if not any(t["id"] == id for t in data["todos"]):
        print(f"❌ 未找到 ID: {id}")
        return
    data["meta"]["current"] = id
    save_data(data)
    print(f"🎯 当前任务已设置为 ID: {id}")
