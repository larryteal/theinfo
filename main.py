import json
import os
import sys
from datetime import datetime, timezone
import curl_cffi


def main(refresh_token: str, install_id: str, login_url: str, briefings_url: str):
    # 构造登录请求 payload
    json_payload = {
        "refresh_token": refresh_token,
        "platform": "android",
        "install_id": install_id,
        "app_version": "2.5.13.2025"
    }

    # 登录获取 JWT
    r = curl_cffi.post(login_url, json=json_payload, impersonate="chrome_android", default_headers=False)
    r.raise_for_status()
    rjson = r.json()
    jwt = rjson["jwt"]

    headers = {
        "Authorization": f"Bearer {jwt}"
    }

    # 获取 briefings 数据
    r = curl_cffi.get(briefings_url, headers=headers, impersonate="chrome", default_headers=False)
    r.raise_for_status()
    data = r.json()

    # 保存到文件
    os.makedirs("./briefings", exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    file_path = f"./briefings/{timestamp}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ Briefings 已保存到 {file_path}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("用法: python main.py [refresh_token] [install_id] [login_url] [briefings_url]")
        sys.exit(1)

    refresh_token = sys.argv[1]
    install_id = sys.argv[2]
    login_url = sys.argv[3]
    briefings_url = sys.argv[4]

    main(refresh_token, install_id, login_url, briefings_url)
