from apscheduler.schedulers.blocking import BlockingScheduler
from main.unit_tracker import run_a_tracker
from main.sendNotify import sendNotify

def build_scheduler(tracking_units):
    # 創建排程器
    scheduler = BlockingScheduler()

    # 設定排程
    for unit in tracking_units:
        scheduler.add_job(run_a_tracker, 'interval', seconds=60, args=[unit])
        print(f"Added job for {unit['dmvNo_name']}")

    scheduler.add_job(sendNotify, 'interval', seconds=30)
    print(f"Added job for sendNotify")

    return scheduler
