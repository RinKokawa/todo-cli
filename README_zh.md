
# 📌 CLI Todo 工具

一个基于 [Typer](https://typer.tiangolo.com/) 开发的命令行待办事项工具，支持嵌套任务、树形结构展示、搜索、时间戳、Git 自动提交、TAPD 导入等功能。

## ✅ 安装

```bash
pip install typer rich
```

## 🚀 快速开始

```bash
todo init                         # 初始化
todo add "完成 README 翻译"        # 添加任务
todo list                        # 树形结构查看任务
todo done 1 -m "翻译完成"          # 标记完成并提交
todo list -a -t                  # 查看所有任务并显示时间
```

## 📂 支持命令

| 命令          | 描述                                |
|---------------|-------------------------------------|
| `init`        | 初始化 todos.json                   |
| `add`         | 添加任务，支持 parent 和自定义 id   |
| `done`        | 标记完成，记录备注和完成时间戳     |
| `list`        | 树形结构显示，支持 -a -t 过滤显示  |
| `delete`      | 删除任务及其所有子任务              |
| `change`      | 修改任务 ID 并更新引用              |
| `rename`      | 修改任务内容                        |
| `search`      | 关键词或 ID 搜索任务                |
| `current`     | 设置当前任务，显示 🎯 高亮标记     |
| `import-tapd` | 从 TAPD 导入任务（CSV）             |

## 🕓 时间戳支持

- 自动记录创建时间 `created_at`
- 自动记录完成时间 `done_at`
- `todo list -t` 显示时间信息

## 📌 作者注

> 项目构建时间：2025-05-11 08:54  
> 开发者自用工具，适合任务管理、Git 集成、项目协作。
