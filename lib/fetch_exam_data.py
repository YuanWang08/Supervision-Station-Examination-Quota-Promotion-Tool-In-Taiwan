import requests
import datetime
from bs4 import BeautifulSoup

def fetch_exam_data(licenseTypeCode, dmvNoLv1, dmvNo):
    # 目標網站的 URL
    url = 'https://www.mvdis.gov.tw/m3-emv-trn/exm/locations'

    # 將西元年轉換為民國年
    roc_year = datetime.datetime.now().year - 1911

    # 格式化日期為民國年格式
    expectExamDateStr = f"{roc_year}{datetime.datetime.now().strftime('%m%d')}"

    # POST 請求的資料
    data = {
        'method': 'query',
        'secDateStr': '',
        'secId': '',
        'divId': '',
        'licenseTypeCode': licenseTypeCode,
        'expectExamDateStr': expectExamDateStr,
        '_onlyWeekend': 'on',
        'dmvNoLv1': dmvNoLv1,
        'dmvNo': dmvNo
    }

    # 發送 POST 請求
    response = requests.post(url, data=data)

    # 檢查請求是否成功
    if response.status_code == 200:
        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到具有 id 為 trnTable 的 table 標籤
        table = soup.find('table', {'id': 'trnTable'})
        if table:
            # 在該 table 標籤內部搜尋 tbody 標籤
            tbody = table.find('tbody')
            if tbody:
                # 初始化一個空的陣列來存放資料
                data_list = []

                # 遍歷 tbody 中的每個 tr 標籤
                for tr in tbody.find_all('tr'):
                    # 找到 tr 中的所有 td 標籤
                    tds = tr.find_all('td')
                    if len(tds) == 4:
                        # 將資料存放到字典中，並移除不需要的換行符號和多餘的空白字符
                        row_data = {
                            'date': tds[0].text.strip(),
                            'desc': tds[1].text.replace('\r', '').replace('\n', '').replace('\t', '').strip(),
                            'number': tds[2].text.strip(),
                        }
                        # 將字典加入到陣列中
                        data_list.append(row_data)

                return data_list
            else:
                print("No <tbody> tag found inside the table with id 'trnTable'.")
        else:
            print("No <table> tag with id 'trnTable' found.")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None