import os
import requests

api_user = os.getenv("TAPD_API_USER")
api_password = os.getenv("TAPD_API_PASSWORD")

def create_story(workspace_id: str, title: str, description: str = ""):
    url = "https://api.tapd.cn/stories"
    payload = {
        "workspace_id": workspace_id,
        "name": title,
        "description": description,
    }

    print(f"📤 正在向项目 {workspace_id} 提交新需求...")
    response = requests.post(url, auth=(api_user, api_password), data=payload)

    print("🌐 状态码:", response.status_code)
    try:
        data = response.json()
        if data.get("status") == 1:
            story = data["data"]["Story"]
            print(f"✅ 创建成功：[{story['id']}] {story['name']}")
        else:
            print("❌ 创建失败:", data.get("info", "无信息"))
    except Exception as e:
        print("❌ 响应解析失败:", e)
        print(response.text)

if __name__ == "__main__":
    workspace_id = "57100817"
    title = "测试提交的新需求"
    description = "<p>这是通过 API 自动创建的需求</p>"

    if not api_user or not api_password:
        print("❌ 未设置环境变量 TAPD_API_USER / TAPD_API_PASSWORD")
    else:
        create_story(workspace_id, title, description)
