# commands/language.py
import typer
import questionary
import json
import os

app = typer.Typer()

CONFIG_FILE = "config.json"

@app.command()
def language():
    '''🌍 语言选择'''
    lang = questionary.select(
        "请选择语言 / Please choose your language:",
        choices=[
            "中文",
            "English",
            "日本語",
            "한국어"
        ]
    ).ask()

    if lang:
        # 保存配置
        # config = {"language": lang}
        # with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        #     json.dump(config, f, ensure_ascii=False, indent=2)

        # 先在这里将配置切换成对应的语言，
        # echo的时候就应该用对应的语言打印了

        typer.echo(f"✅ 当前语言设置为：{lang}")
    else:
        typer.echo("❌ 取消选择")

