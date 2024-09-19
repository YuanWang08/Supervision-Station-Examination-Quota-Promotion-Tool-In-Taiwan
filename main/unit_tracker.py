from lib.format_exam_data import getFormattedExamData
from crud.put_data_in_database import process_data

def run_a_tracker(unit):
    # 獲取格式化後的考試資料
    formatted_data = getFormattedExamData(unit['typeOfTest_name'], unit['dmvNoLv1_name'], unit['dmvNo_name'])
    # 將資料寫入資料庫
    process_data(formatted_data)
