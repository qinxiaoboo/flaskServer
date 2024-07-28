
from flaskServer.config.connect import db

class TaskRecord(db.Model):
    __tablename__  = "t_task_record"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    env_name = db.Column(db.String(120), unique=True, nullable=False)
    # 任务状态：0：已完成，1：默认值
    status = db.Column(db.Integer, unique=False, nullable=True)

    # __mapper_args__ = {
    #     "order_by": env_name.desc()
    # }