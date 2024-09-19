import requests
import json

# Webhook URL
webhook_url = 'https://discord.com/api/webhooks/1261362213315285043/bciSXho_7o2K6k7ZmNvfEGP5RLV1Y1oF7pbxUuyg5HRQRRmVdb4pzdk_lpd8u_AhBsBx'

# 發送訊息的函數
def send_discord_message(content):
    data = {
        "content": content,
        "username": "John Doe",
    }

    # 發送請求到 Discord Webhook
    response = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    
    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")

