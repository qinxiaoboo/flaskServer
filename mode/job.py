from flaskServer.config.connect import db
# from dataclasses import dataclass
#
# from dataclasses_json import dataclass_json
#
#
# @dataclass_json
# @dataclass
class Job(db.Model):
    __tablename__="t_job"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    trigger = db.Column(db.String(20), nullable=False)  # e.g., 'cron', 'interval'
    hour = db.Column(db.Integer)
    minute = db.Column(db.Integer)
    function_name = db.Column(db.String(80), nullable=False)
    parameters = db.Column(db.String(200))  # JSON serialized string
    interval = db.Column(db.Integer)  # Interval in minutes
    interval_unit = db.Column(db.String(10))  # Unit of interval ('seconds', 'minutes', etc.)
    groups = db.Column(db.String(10))

    def to_dict(job):
        return {
            'id': job.id,
            'name': job.name,
            'trigger': job.trigger,
            'hour': job.hour,
            'minute': job.minute,
            'function_name': job.function_name,
            'parameters': job.parameters,
            'interval': job.interval,
            'interval_unit': job.interval_unit,
            'groups': job.groups
        }