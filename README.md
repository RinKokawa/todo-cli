# 📁 .todo 仓库系统设计文档

> 更新时间：UTC/GMT+08:00 2025-05-11 17:42

---

## ✅ 项目简介

本 CLI Todo 工具使用 Python + Typer 实现，具备任务添加、嵌套展示、状态切换、隐藏标记、搜索等能力。为进一步支持**误操作恢复**、**版本管理**，预留 `.todo/` 目录作为内部仓库机制，类似于 Git 的 `.git/`。

---

## 📦 .todo 目录结构设计

```bash
.todo/
├── snapshots/                 # 每次修改前的 todos.json 快照副本
│   ├── 20250511T094124.json
├── HEAD                       # 指向当前快照文件名（可选）
├── log.txt                    # 每次操作记录日志（可选）
├── config.json                # 配置文件（可用于开关自动备份）
```

---

## 🛠 快照策略

- 所有 **写操作命令**（如 `add`, `delete`, `rename`, `done` 等）在执行前自动备份 `todos.json`。
- 快照文件保存至 `.todo/snapshots/{timestamp}.json`，使用 `ISO8601` 时间戳命名。

---

## 🧩 已实现功能列表（核心功能）

| 功能            | 命令说明                                              |
|-----------------|-------------------------------------------------------|
| 添加任务        | `todo add "任务内容"`                                  |
| 任务完成        | `todo done [id] -m "完成备注"`                          |
| 修改内容        | `todo rename [id] "新内容"`                             |
| 删除任务        | `todo delete [id]`（递归删除其所有子任务）             |
| 修改 ID         | `todo change [旧id] [新id]`                             |
| 设置当前        | `todo current [id]` 设置当前任务                        |
| 隐藏任务        | `todo hide [id]` / `todo hide [id] --unhide`           |
| 搜索任务        | `todo search [关键词|id]`                               |
| 树形展示        | `todo list`（支持 `-a`, `-t`, `--only-xxx` 多种过滤）   |
| TAPD 导入       | `todo import-tapd 文件.csv`                             |

---

## 🚧 预留功能规划

| 功能              | 描述                                           |
|-------------------|------------------------------------------------|
| `todo undo`       | 恢复上一个快照版本                             |
| `todo log`        | 查看操作历史记录                                |
| `todo restore X`  | 恢复到某个特定版本的 todos.json                 |
| `todo config`     | 设置是否启用自动快照、最大保留历史数等          |

---

## 🧠 示例 log.txt 内容（计划格式）

```
2024-05-11T17:58:12 add ID 42: 写README
2024-05-11T17:59:30 done ID 42
2024-05-11T18:00:12 delete ID 42 and 2 children
```

---

## 📌 作者提示

当前 `.todo/` 尚未实际写入，所有设计为**可扩展性预留**，实现该机制后可为 CLI 提供完整任务版本管理与撤销功能。
