
# 📌 CLI Todo CLI Tool

A command-line todo manager built with [Typer](https://typer.tiangolo.com/), featuring nested tasks, tree display, timestamps, search, Git auto-commit, and TAPD import support.

## ✅ Installation

```bash
pip install typer rich
```

## 🚀 Quick Start

```bash
todo init
todo add "Translate README to English"
todo list
todo done 1 -m "Translation done"
todo list -a -t
```

## 📂 Commands

| Command       | Description                                  |
|---------------|----------------------------------------------|
| `init`        | Initialize todos.json                        |
| `add`         | Add a task with optional parent or custom ID |
| `done`        | Mark task as done, record time & message     |
| `list`        | Show tasks in tree view (-a/-t supported)    |
| `delete`      | Delete task and its children                 |
| `change`      | Change task ID and update dependencies       |
| `rename`      | Modify task text                             |
| `search`      | Search by keyword or ID                      |
| `current`     | Set current task (🎯 highlight)              |
| `import-tapd` | Import tasks from TAPD CSV                   |

## 🕓 Timestamp Support

- `created_at`: recorded when task is added
- `done_at`: recorded when task is marked done
- View with `todo list -t`

## 📌 Author's Note

> Generated: 2025-05-11 08:54  
> CLI tool for personal task & project tracking with Git integration.
