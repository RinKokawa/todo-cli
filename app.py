# app.py（新的 Typer 入口）
import typer
from commands.list import list as list_command
from commands.add import add as add_command
from commands.done import done as done_command
from commands.init import init as init_command
from commands.delete import delete as delete_command
from commands.current import current as current_command
from commands.change import change as change_command
from commands.import_tapd import import_tapd as import_tapd_command

# app.py 中追加注册rename
from commands.rename import rename as rename_command

app = typer.Typer(help="📌 一个简单的 CLI Todo 工具，支持嵌套任务与树形结构展示。")

app.command()(list_command)
app.command()(add_command)
app.command()(done_command)
app.command()(init_command)
app.command()(delete_command)
app.command()(current_command)
app.command()(change_command)
app.command()(import_tapd_command)

app.command()(rename_command)

if __name__ == "__main__":
    app()
