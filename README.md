<!--
  README.md for the “todo” CLI project
-->

# 📌 Task CLI
[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](#)  [![License](https://img.shields.io/badge/license-MIT-green.svg)](#) [![观看演示](https://img.shields.io/badge/视频演示-点击观看-red?logo=YouTube)](https://www.youtube.com/watch?v=dQw4w9WgXcQ) [![Bilibili 演示](https://img.shields.io/badge/B站视频-点击观看-pink?logo=bilibili)](https://www.bilibili.com/video/BV1GJ411x7h7/)




一个基于 [Typer](https://typer.tiangolo.com/) 与 [Rich](https://rich.readthedocs.io/) 的命令行 Todo 工具，支持任务嵌套、树形展示、优先级象限、隐藏与搜索、Git 自动提交以及 TAPD CSV 导入。

---

## 🚀 快速开始

### 安装

```bash
# 建议使用虚拟环境
pip install todo-task-node-tree
```

> 如果是通过git克隆的，可在项目根目录执行：
> 
> ```bash
> pip install .
> ```

### 初始化

```bash
# 在当前目录创建数据文件 todos.json
todo init
```

### 添加任务

```bash
# 添加一级任务
todo add "写 README"
# 添加子任务，parent 指定父任务 ID
todo add "完善命令帮助文档" -p 1
# 指定优先级象限（1=🔥紧急重要・2=🧭重要・3=📤紧急・4=❌低优先，默认 2）
todo add "发布 PyPI 包" -q 1
```

### 列表展示

```bash
# 默认展示未完成任务，树形结构
todo list

# 显示所有任务（包括已完成、隐藏）
todo list --all

# 只看已完成
todo list --only-done

# 只看隐藏
todo list --only-hidden

# 高亮象限
todo list -q
```

### 设置当前任务

```bash
todo current 3
# “当前”任务会被特殊标记，便于聚焦
```

### 完成任务

```bash
# 标记任务为完成，自动记录 done 时间戳
todo done 2 5 --message "已完成当日目标"
```

> 若在 Git 仓库中执行，工具会自动 `git add . && git commit -m "完成任务 …"` 并 `git push`。

### 其他常用命令

| 命令 | 说明 |
| --- | --- |
| `todo delete <ID>` | 删除指定任务及所有子任务 |
| `todo change <旧ID> <新ID>` | 修改任务 ID |
| `todo rename <ID> <新内容>` | 修改任务文本内容 |
| `todo move <ID> <新父ID>` | 移动任务到另一父任务（0 代表顶层） |
| `todo hide <ID>…` | 隐藏 / 取消隐藏 任务 |
| `todo search <关键词>` | 按 ID 或文本模糊搜索 |
| `todo stats` | 统计各象限已完成/未完成数量 |
| `todo import-tapd <CSV>` | 从 TAPD 导出的 CSV 文件批量导入任务 |

---

## 📂 数据存储

-   默认在运行目录下创建并维护 `todos.json`。
    
-   存储格式：
    
    ```json
    {
      "meta": {
        "current": 3
      },
      "todos": [
        {
          "id": 1,
          "text": "写 README",
          "parent": null,
          "quadrant": 2,
          "created_at": "2025-05-25T15:00:00",
          "done": false,
          "done_at": null,
          "hidden": false
        },
        …
      ]
    }
    ```
    

---

## 🛠️ 开发 & 发布

1.  **环境准备**
    
    ```bash
    python -m venv .venv
    source .venv/bin/activate    # Linux / macOS
    .venv\Scripts\activate.bat   # Windows
    pip install -r requirements.txt
    ```
    
2.  **项目结构**
    
    ```bash
    .
    ├── app.py                 # Typer 主入口（`todo` 命令）
    ├── main.py                # 内部实现（保留兼容）
    ├── commands/              # 各子命令实现
    ├── core/                  # 数据与 Git 工具模块
    ├── todos.json             # 默认数据文件
    ├── README.md              # 本文件
    └── setup.py / pyproject.toml  # 打包配置（待添加）
    ```
    
3.  **运行测试**
    
    > 如有测试可在此补充，如使用 `pytest`。
    
    ```bash
    pytest
    ```
    
4.  **打包 & 上传 PyPI**
    
    -   **使用 `setup.py`**：
        
        ```bash
        python setup.py sdist bdist_wheel
        twine upload dist/*
        ```
        
    -   **使用 `pyproject.toml` + Poetry**：
        
        ```bash
        poetry build
        poetry publish --username <用户名> --password <密码>
        ```
        

---

## 🤝 贡献

欢迎提交 Issue 或 PR！

1.  Fork 本仓库
    
2.  新建分支 `feat/your-feature`
    
3.  提交代码 & 测试
    
4.  发起 Pull Request
    

---

## 📄 License

本项目采用 [MIT License](LICENSE) —— 详情请查看 `LICENSE` 文件。
