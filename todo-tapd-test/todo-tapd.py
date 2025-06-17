import os
import requests
from collections import defaultdict

# 从环境变量中读取 TAPD API 用户名和密码
api_user = os.getenv("TAPD_API_USER")
api_password = os.getenv("TAPD_API_PASSWORD")
workspace_id = "57100817"

# 状态码映射表
STATUS_MAP = {
    "status_0": "新建",
    "status_1": "设计中",
    "status_2": "开发中",
    "status_3": "测试中",
    "status_4": "已上线",
    "status_14": "已完成",
    "status_7": "关闭",
    "planning": "规划中"
}

# 获取需求列表
def fetch_stories(workspace_id):
    url = "https://api.tapd.cn/stories"
    params = {
        "workspace_id": workspace_id,
        "limit": 200
    }

    response = requests.get(url, auth=(api_user, api_password), params=params)
    if response.status_code != 200:
        print("❌ 请求失败")
        return []

    data = response.json()
    if data.get("status") != 1:
        print("❌ API 返回错误:", data.get("info"))
        return []

    return [item["Story"] for item in data.get("data", [])]

# 构建父子结构树
def build_tree(stories):
    story_map = {s["id"]: s for s in stories}
    children_map = defaultdict(list)

    for story in stories:
        pid = story.get("parent_id")
        if pid and pid in story_map and pid != story["id"]:
            children_map[pid].append(story)
        else:
            children_map[None].append(story)  # 根节点（无父）

    return children_map

# 打印树状结构
def print_tree(children_map, parent_id=None, level=0, index_prefix=""):
    children = children_map.get(parent_id, [])
    for i, story in enumerate(children, 1):
        index = f"{index_prefix}{i}" if index_prefix else str(i)
        indent = "    " * level
        status = STATUS_MAP.get(story.get("status", ""), story.get("status", ""))
        creator = story.get("creator", "未知")
        created = story.get("created", "未知时间")
        # modified = story.get("modified", "未知时间")
        print(f"{indent}{index}. [{status}] {story.get('name')}（创建人: {creator}, 创建时间: {created}）")
        print_tree(children_map, story["id"], level + 1, index + ".")

# 主流程
def get_stories_as_tree(workspace_id):
    print(f"📡 正在获取项目（ID: {workspace_id}）的需求...")
    stories = fetch_stories(workspace_id)
    if not stories:
        print("⚠️ 无数据")
        return

    children_map = build_tree(stories)
    print(f"\n📋 共获取 {len(stories)} 条需求，按树状结构打印如下：\n")
    print_tree(children_map)

if __name__ == "__main__":
    print("🚀 启动 TAPD 树状结构需求打印程序")
    if not api_user or not api_password:
        print("❌ 未设置 TAPD_API_USER 或 TAPD_API_PASSWORD 环境变量")
    else:
        get_stories_as_tree(workspace_id)
