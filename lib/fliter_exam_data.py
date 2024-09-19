from lib.fetch_exam_data import fetch_exam_data

def filter_exam_data(licenseTypeCode, dmvNoLv1, dmvNo):
    exam_data = fetch_exam_data(licenseTypeCode, dmvNoLv1, dmvNo)

    # 只留下 'number' 不是 '額滿' 的資料
    filtered_data = [item for item in exam_data if item['number'] != '額滿']

    return filtered_data

# 測試函數
if __name__ == "__main__":
    filtered_data = filter_exam_data()

    # 輸出結果
    if filtered_data:
        for item in filtered_data:
            print(item)