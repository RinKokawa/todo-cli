# commands/init.py
import typer
from rich import print
from core.data import DATA_FILE, save_data

app = typer.Typer()

@app.command(help="🧱 初始化 todos.json 文件")
def init():
    """🔛 初始化功能：初始化 todos.json 文件"""
    if DATA_FILE.exists():
        print("✅ todos.json 已存在")
    else:
        save_data({"meta": {}, "todos": []})
        print("📁 已初始化空的 todos.json")
