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
from commands.rename import rename as rename_command
from commands.search import search as search_command
from commands.hide import hide as hide_command
from commands.stats import stats as stats_command

from commands.move import move as move_command
from commands.language  import  language as language_command



app = typer.Typer(
    help="📌 一个简单的 CLI Todo 工具，支持嵌套任务与树形结构展示。",
    invoke_without_command=True
)

@app.callback()
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())

app.command()(init_command)

app.command()(list_command)
app.command()(add_command)

app.command()(done_command)
# 增加do别名
app.command(name="do",help = "✅ done的别名")(done_command)


app.command()(delete_command)
# 增加rm别名
app.command(name="rm",help = "❌ 删除的别名")(delete_command)
app.command()(current_command)
app.command()(change_command)
app.command()(rename_command)

app.command()(search_command)
# ✅ 给 search 添加别名 find
app.command(name="find",help = "🔍 search别名")(search_command)

app.command()(hide_command)
app.command()(stats_command)
app.command()(move_command)

app.command()(import_tapd_command)

app.command()(language_command)



if __name__ == "__main__":
    app(prog_name="todo")
