# date: 時間Int化 例：113年10月17日 (星期四) -> 1131017
# date_chinese: 時間中文化 例：113年10月17日
# day_of_week: 星期幾 例：四
# supervision_area: 例：臺中區監理所(中彰投)
# supervision_unit: 例：埔里監分站
# license_type: 例：普通重型機車
# remaining_places: 剩餘名額 例：3
# description: 例：上午場次, 組別 1本場次為初次報考機車(含輕型)駕照之考生，請先完成體檢並於8:30前報到繳費
# record_time: 紀錄時間 例：2021-10-17 14:00:00

from lib.fliter_exam_data import filter_exam_data
import datetime

# 導入資料
from data.licenseTypeCode import licenseTypeCode
from data.dmv_data import dmvNoLv1, dmvNo

def getIntTime(date):
    # 使用 split 方法解析日期
    parts = date.split('年')
    year = parts[0]
    month_day = parts[1].split('月')
    month = month_day[0]
    day = month_day[1].split('日')[0]

    # 將解析出的部分組合成整數格式後轉換成字串
    return str(int(year + month.zfill(2) + day.zfill(2)))

def getDateChinese(date):
    # 使用 split 方法解析日期
    parts = date.split('年')
    year = parts[0]
    month_day = parts[1].split('月')
    month = month_day[0]
    day = month_day[1].split('日')[0]

    # 將解析出的部分組合成所需的格式
    return f"{year}年{month.zfill(2)}月{day.zfill(2)}日"

def getDayOfWeek(date):
    # 使用 split 方法解析日期
    parts = date.split('年')
    year = int(parts[0]) + 1911  # 將民國年轉換為西元年
    month_day = parts[1].split('月')
    month = int(month_day[0])
    day = int(month_day[1].split('日')[0])

    # 使用 datetime 模組來取得星期幾
    date_obj = datetime.date(year, month, day)
    day_of_week = date_obj.strftime('%A')  # 取得英文的星期幾

    # 將英文的星期幾轉換為中文
    day_of_week_map = {
        'Monday': '一',
        'Tuesday': '二',
        'Wednesday': '三',
        'Thursday': '四',
        'Friday': '五',
        'Saturday': '六',
        'Sunday': '日'
    }

    return day_of_week_map[day_of_week]

def getFormattedExamData(typeOfTest_name, dmvNoLv1_name, dmvNo_name):
    formatted_exam_data = []

    typeOfTest_code = licenseTypeCode[typeOfTest_name]
    dmvNoLv1_code = dmvNoLv1[dmvNoLv1_name]
    dmvNo_code = dmvNo[dmvNo_name]

    exam_data = filter_exam_data(typeOfTest_code, dmvNoLv1_code, dmvNo_code)

    for item in exam_data:
        date = getIntTime(item['date'])
        date_chinese = getDateChinese(item['date'])
        day_of_week = getDayOfWeek(item['date'])
        supervision_area = dmvNoLv1_name
        supervision_unit = dmvNo_name
        license_type = typeOfTest_name
        remaining_places = item['number']
        description = item['desc']
        record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        formatted_exam_data.append({
            'date': date,
            'date_chinese': date_chinese,
            'day_of_week': day_of_week,
            'supervision_area': supervision_area,
            'supervision_unit': supervision_unit,
            'license_type': license_type,
            'remaining_places': remaining_places,
            'description': description,
            'record_time': record_time
        })
    print(formatted_exam_data)
    return formatted_exam_data