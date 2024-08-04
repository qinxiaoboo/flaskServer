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
        tasks = dict()
        for t in ts:
            if t.env_name in tasks:
                tasks[t.env_name].append({f"{t.name}": "未完成" if t.status == 0 else "完成"})
            else:
                tasks[t.env_name] = [{f"{t.name}": "未完成" if t.status == 0 else "完成"}]
        for key, value in tasks.items():
            dicts = dict()
            dicts["环境"] = key
            for data in value:
                for name, vv in data.items():
                    dicts[f"{name}"] = f"{vv}"
            print(dicts)
            r.add_data(dicts)
    r.record()


if __name__ == '__main__':
    initTaskList()