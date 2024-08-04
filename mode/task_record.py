import datetime

from flaskServer.config.connect import db

class TaskRecord(db.Model):
    __tablename__  = "t_task_record"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    env_name = db.Column(db.String(120), unique=True, nullable=False)
    # 任务状态：1：已完成，0：默认值
    status = db.Column(db.Integer, unique=False, nullable=True)
    count = db.Column(db.Integer, unique=False, nullable=True)
    createtime = db.Column(db.DateTime, default=datetime.datetime.now(),comment="创建时间")
    updatetime = db.Column(db.DateTime, default=datetime.datetime.now(),comment="更新时间")
    #

    # __mapper_args__ = {
    #     "order_by": env_name.desc()
    # }