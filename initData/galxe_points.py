import shutil

from DataRecorder import Recorder
from flaskServer.config.config import ENV_PATH
from flaskServer.config.connect import app,db
from flaskServer.mode.space_points import SpacePoints
from pathlib import Path
from datetime import datetime

def init():
    p = Path(ENV_PATH).parent / 'points.csv'
    if p.exists():
        shutil.move(p, p.parent / f"task_{datetime.now().strftime('%Y_%m_%d(%H_%M)')}.csv")
    r = Recorder(path=p ,cache_size=20)
    r.set.fit_head(True)
    with app.app_context():
        ts = db.session.query(SpacePoints).order_by(SpacePoints.env_name.asc()).all()
        points = {}
        for t in ts:
            if t.env_name in points:
                points[t.env_name].append({f"{t.name}-{t.alia}":f"{t.points}:{t.ranking}"})
            else:
                points[t.env_name] = [{f"{t.name}-{t.alia}":f"{t.points}:{t.ranking}"}]
        for key,value in points.items():
            dicts = dict()
            dicts["环境"] = key
            for data in value:
                for name,vv in data.items():
                    dicts[f"{name}"] = f"{vv}"
            r.add_data(dicts)
    r.record()
    return p


if __name__ == '__main__':
    init()