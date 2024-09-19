from crud.get_and_delete_shortDb import get_and_delete_shortDb
from discord.discord_webhook import send_discord_message    
import datetime
import json
import os

# 獲取 config.json 的絕對路徑
config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')

# 讀取 config.json 檔案
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

trackingDuration = config['trackingDuration']

def checkIfMeetRequirement(data, trackingDuration):
    current_date = datetime.datetime.now()
    max_date = current_date + datetime.timedelta(days=trackingDuration)
    
    # 將 ROC 年轉換為西元年
    def roc_to_gregorian(roc_date_str):
        roc_year = int(roc_date_str[:3])
        gregorian_year = roc_year + 1911
        return f"{gregorian_year}{roc_date_str[3:]}"
    
    filtered_data = []
    for item in data:
        exam_date_str = item[1]  # 假設日期在第二個欄位
        exam_date = datetime.datetime.strptime(roc_to_gregorian(exam_date_str), '%Y%m%d')
        if current_date <= exam_date <= max_date:
            filtered_data.append(item)
    
    return filtered_data

def sendNotify():
    data = get_and_delete_shortDb()
    data = checkIfMeetRequirement(data, trackingDuration)
    max_items_per_message = 8
    content_template = "🔥 發現空缺名額啦 🔥\n"
    content_suffix = "趕快去預約吧！"

    # 將資料分成多個訊息，每個訊息最多包含 max_items_per_message 組資料
    for start in range(0, len(data), max_items_per_message):
        content = content_template
        for i in data[start:start + max_items_per_message]:
            content += (
                f"📅 日期：{i[2]} ({i[3]})\n"
                f"🗺️ 地點：{i[5]}\n"
                f"👨‍✈️ 類別：{i[6]}\n"
                f"🈶 剩餘名額：{i[7]}\n"
                f"💬 說明：{i[8]}\n"
                f"----------------\n"
            )
        content += content_suffix
        print(content)
        send_discord_message(content)
