
# 📌 CLI型Todo管理ツール

[Typer](https://typer.tiangolo.com/) 製のコマンドラインTodo管理ツールです。階層付きタスク、ツリー表示、検索、タイムスタンプ、Git自動コミット、TAPDインポートなどをサポート。

## ✅ インストール

```bash
pip install typer rich
```

## 🚀 クイックスタート

```bash
todo init
todo add "READMEの日本語翻訳を完了する"
todo list
todo done 1 -m "翻訳完了"
todo list -a -t
```

## 📂 利用可能なコマンド

| コマンド       | 説明                                          |
|----------------|-----------------------------------------------|
| `init`         | todos.json の初期化                           |
| `add`          | タスク追加、親ID・任意ID指定可能             |
| `done`         | タスク完了のマーク、完了メッセージ記録       |
| `list`         | ツリー形式で表示、-a/-tで詳細制御可能        |
| `delete`       | タスクとその子タスクを削除                   |
| `change`       | タスクIDの変更と依存関係の更新               |
| `rename`       | タスク内容を編集                             |
| `search`       | キーワードまたはIDで検索                     |
| `current`      | 現在のタスクを設定、🎯 ハイライト表示        |
| `import-tapd`  | TAPD CSVファイルからインポート               |

## 🕓 タイムスタンプ機能

- `created_at`：タスク作成時に記録
- `done_at`：完了時に記録
- `todo list -t` で表示可能

## 📌 作者より

> 生成日：2025-05-11 08:54  
> Git連携や開発タスク管理に最適なCLIツール。
