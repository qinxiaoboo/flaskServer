from flaskServer.config.connect import db,app

class TaskLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    env_name = db.Column(db.String(50), nullable=False)
    task_name = db.Column(db.String(255), nullable=False)
    # 任务结果
    task_result = db.Column(db.Text)
    # 任务执行消息
    execution_result = db.Column(db.Text)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    # 任务进行状态
    status = db.Column(db.Enum('pending', 'running', 'completed', 'cancelled'), default='pending')

    def to_dict(self):
        return {
            'id': self.id,
            'env_name': self.env_name,
            'task_name': self.task_name,
            'task_result': self.task_result,
            'execution_result': self.execution_result,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'status': self.status
        }

if __name__ == '__main__':

    # Create the database and table
    with app.app_context():
        db.create_all()