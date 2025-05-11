# commands/import_tapd.py
import typer
import csv
from pathlib import Path
from rich import print
from core.data import load_data, save_data

app = typer.Typer()

@app.command(help="📥 从 TAPD CSV 导入任务")
def import_tapd(
    csv_file: Path = typer.Argument(..., help="TAPD 导出的 CSV 文件路径")
):
    data = load_data()
    todos = data["todos"]

    with open(csv_file, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
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
