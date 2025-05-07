
# 📌 CLI Todo 工具

一个基于 [Typer](https://typer.tiangolo.com/) 的命令行待办事项工具，支持嵌套任务、树形结构展示、TAPD 任务导入、Git 自动提交等功能。

---

## ✅ 安装依赖

```bash
pip install typer rich
```

如需支持 `.xlsx`，额外安装：

```bash
pip install openpyxl
```

---

## 🚀 快速开始

```bash
python main.py init                 # 初始化 todos.json
python main.py add "实现登录功能"     # 添加任务
python main.py list                # 显示任务树
python main.py done 1 -m "已完成登录开发"  # 标记任务完成 + Git 提交
```

---

## 📂 功能命令

| 命令             | 描述                                      |
|------------------|-------------------------------------------|
| `init`           | 初始化 todos.json 文件                    |
| `add`            | 添加一个任务，支持 --parent / --id        |
| `list`           | 树形结构显示任务，支持 --all 显示已完成   |
| `done`           | 标记任务为完成，可加备注并自动 Git 提交   |
| `delete`         | 删除任务及其所有子任务                    |
| `change`         | 修改任务 ID，自动更新引用关系              |
| `current`        | 设置当前任务，列表中高亮显示              |
| `import-tapd`    | 从 TAPD 导出的 CSV 文件导入任务            |

---

## 📥 TAPD 导入

### 1. 导出 CSV（包含字段）

| ID | 标题 | 状态 | 父需求 |
|----|------|------|--------|

### 2. 导入命令

```bash
python main.py import-tapd ./hunter.csv
```

- 自动识别父子关系（基于“父需求”字段）
- 状态包含“完成”“关闭”将自动标记为完成
- 自动跳过已存在的 ID

---

## 📁 数据结构示例（todos.json）

```json
{
  "meta": {
    "current": 3
  },
  "todos": [
    { "id": 1, "text": "首页搭建", "parent": null, "done": true },
    { "id": 2, "text": "接入微信登录", "parent": 1, "done": false }
  ]
}
```

---

## 📌 作者

> 自用 CLI 待办管理脚本，适合结合 Git 提交日常项目进度。  
> 欢迎二次开发和定制。
