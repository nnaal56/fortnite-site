import os
import requests
import json
from datetime import datetime

# سحب البيانات بأمان من بيئة التشغيل
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = "nnaal56/fortnite-site"

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def update_site_leaks(leak_content, chat_id):
    file_path = "leaks.json"
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{file_path}"
    
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    
    response = requests.get(url, headers=headers)
    sha = ""
    leaks_list = []
    
    if response.status_code == 200:
        file_data = response.json()
        sha = file_data["sha"]
        import base64
        decoded_content = base64.b64decode(file_data["content"]).decode("utf-8")
        leaks_list = json.loads(decoded_content)
    
    new_leak = {
        "content": leak_content,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    leaks_list.insert(0, new_leak)
    
    updated_content_str = json.dumps(leaks_list, ensure_ascii=False, indent=4)
    encoded_content = base64.b64encode(updated_content_str.encode("utf-8")).decode("utf-8")
    
    data = {
        "message": "إضافة تسريب جديد عبر بوت التلجرام الآلي 🤖",
        "content": encoded_content,
        "sha": sha
    }
    
    put_response = requests.put(url, headers=headers, json=data)
    
    if put_response.status_code in [200, 201]:
        send_telegram_message(chat_id, "🔥 تم نشر التسريب بنجاح على موقعك وتحديثه أوتوماتيكياً!")
    else:
        send_telegram_message(chat_id, f"⚠️ حدث خطأ أثناء الرفع: {put_response.text}")
