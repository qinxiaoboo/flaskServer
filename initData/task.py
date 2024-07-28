import time
import shutil

from DataRecorder import Recorder
from flaskServer.config.config import ENV_PATH
from flaskServer.config.connect import app,db
from flaskServer.mode.task_record import TaskRecord
from pathlib import Path
from datetime import datetime

def initTaskList():
    p = Path(ENV_PATH).parent / 'task.csv'
    if p.exists():
        shutil.move(p, p.parent / f"task_{datetime.now().strftime('%Y_%m_%d(%H_%M)')}.csv")
    r = Recorder(path=p ,cache_size=20)
    r.set.fit_head(True)
    with app.app_context():
        ts = db.session.query(TaskRecord).order_by(TaskRecord.env_name.asc()).all()
        for t in ts:
            r.add_data({"环境": t.env_name,f"{t.name}": "完成" if t.status == 0 else "未完成"})
            print(f"{t.name} {t.env_name} {t.status}")
    r.record()
    print(r.show_msg)


if __name__ == '__main__':
    initTaskList()