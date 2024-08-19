import shutil
from datetime import datetime
from pathlib import Path

from DataRecorder import Recorder

from flaskServer.config.config import ENV_PATH
from flaskServer.services.dto.task_record import getTaskRecordInfo


def initTaskList():
    p = Path(ENV_PATH).parent / 'task.csv'
    if p.exists():
        shutil.move(p, p.parent / f"task_{datetime.now().strftime('%Y_%m_%d(%H_%M)')}.csv")
    r = Recorder(path=p ,cache_size=20)
    r.set.fit_head(True)
    for dicts in getTaskRecordInfo():
        r.add_data(dicts)
    r.record()


if __name__ == '__main__':
    initTaskList()