from lib.format_exam_data import getFormattedExamData
from schedulers.auto_fetch_data import build_scheduler
from db.mysql import connect_mysql, check_and_create_table
from db.redis import connect_redis
import json
import os

# 獲取 config.json 的絕對路徑
config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.json')

# 讀取 config.json 檔案
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

trackingUnits = config['trackingUnits']
print(trackingUnits)

# 資料庫配置
db_config = {
    'user': 'root',
    'password': 'my-secret-pw',
    'host': 'localhost',
    'port': 3300,
    'database': 'test_db',
    'autocommit': True,  # Ensures immediate commit
    'connection_timeout': 1200,  # Set an appropriate timeout
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}

# Redis 配置
redis_config = {
    'host': 'localhost',
    'port': 6379,
    'db': 0
}

# 測試資料庫連接
db_conn, db_cursor = connect_mysql(db_config)

# 檢查並創建資料表--long_term_data
create_long_term_data_table_sql = """
CREATE TABLE long_term_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date VARCHAR(255),
    date_chinese VARCHAR(255),
    day_of_week VARCHAR(255),
    supervision_area VARCHAR(255),
    supervision_unit VARCHAR(255),
    license_type VARCHAR(255),
    remaining_places INT,
    description TEXT,
    record_time DATETIME
)
"""
check_and_create_table(db_cursor, 'long_term_data', create_long_term_data_table_sql)

# 檢查並創建資料表--push_data
create_push_data_table_sql = """
CREATE TABLE push_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date VARCHAR(255),
    date_chinese VARCHAR(255),
    day_of_week VARCHAR(255),
    supervision_area VARCHAR(255),
    supervision_unit VARCHAR(255),
    license_type VARCHAR(255),
    remaining_places INT,
    description TEXT,
    record_time DATETIME
)
"""
check_and_create_table(db_cursor, 'push_data', create_push_data_table_sql)

# 關閉資料庫連接
db_cursor.close()
db_conn.close()

# 建立 Redis 連接
# redis_conn = connect_redis(redis_config)

# 創建排程器
scheduler = build_scheduler(trackingUnits)

# 開始排程
try:
    print("Scheduler started. Fetching data every 60 seconds...")
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("Scheduler stopped.")