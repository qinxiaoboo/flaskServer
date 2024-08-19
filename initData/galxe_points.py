import shutil

from DataRecorder import Recorder
from flaskServer.config.config import ENV_PATH
from flaskServer.services.dto.galxeAccount import getGaxlesInfo
from pathlib import Path
from datetime import datetime

def init():
    p = Path(ENV_PATH).parent / 'points.csv'
    if p.exists():
        shutil.move(p, p.parent / f"points_{datetime.now().strftime('%Y_%m_%d(%H_%M)')}.csv")
    r = Recorder(path=p, cache_size=20)
    r.set.fit_head(True)
    for dicts in getGaxlesInfo():
        r.add_data(dicts)
    r.record()
    return p


if __name__ == '__main__':
    init()