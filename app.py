# app.py（新的 Typer 入口）
import typer
from commands import add, done, list, init, delete, current, change, import_tapd

app = typer.Typer(help="📌 一个简单的 CLI Todo 工具，支持嵌套任务与树形结构展示。")

app.add_typer(add.app, name="add")
app.add_typer(done.app, name="done")

from commands.list import list as list_command
app.command()(list_command)

app.add_typer(init.app, name="init")
app.add_typer(delete.app, name="delete")
app.add_typer(current.app, name="current")
app.add_typer(change.app, name="change")
app.add_typer(import_tapd.app, name="import-tapd")

if __name__ == "__main__":
    app()
