import json
import socket
from flaskServer.mode.job import Job
from flaskServer.config.connect import db, app
from flaskServer.config.scheduler import *
from flaskServer.services.dto.dataDictionary import getDataDictionaryByValue
from sqlalchemy import and_



def schedule_job(job_id, function_name, parameters, hour, minute, interval, interval_unit):
    def job_function():
        func = get_function_by_name(function_name)
        if func:
            if parameters:
                params = parameters.split(",")
            else:
                params = []
            print(params)
            func(*params)
        else:
            print(f"Function {function_name} not found")

    if interval and interval_unit:
        scheduler.add_job(
            func=job_function,
            trigger='interval',
            minutes=interval if interval_unit == 'minutes' else None,
            seconds=interval if interval_unit == 'seconds' else None,
            id=str(job_id)
        )
    else:
        scheduler.add_job(
            func=job_function,
            trigger='cron',
            hour=hour,
            minute=minute,
            id=str(job_id)
        )

def getJobByName(name):
    with app.app_context():
        job = Job.query.filter_by(name=name).first()
    return job

def getJobs(groups):
    List  =[]
    with app.app_context():
        # if groups == "all":
        #     jobs = Job.query.all()
        # else:
        jobs = Job.query.filter_by(groups=groups).all()
        for job in jobs:
            List.append(job.to_dict())
    return List

def getJob(groups,job_id):
    with app.app_context():
        job = Job.query.filter(and_(Job.groups==groups,Job.id==job_id)).first()
    return job.to_dict()

def deleteJob(job_id):
    with app.app_context():
        job = Job.query.get(job_id)
        if job:
            db.session.delete(job)
            db.session.commit()
            scheduler.remove_job(job_id)

def updateJob(data):
    name = data.get("name")
    job = getJobByName(name)
    trigger=data.get("trigger")
    hour = data.get("hour")
    minute = data.get("minute")
    function_name = data.get("function_name")
    parameters = data.get("parameters", [])
    interval = data.get("interval")
    interval_unit = data.get("interval_unit")
    groups = data.get("groups")
    with app.app_context():
        if job:
            scheduler.remove_job(str(job.id))
            if trigger and job.trigger != trigger:
                job.trigger = trigger
            if hour and job.hour != hour:
                job.hour = hour
            if minute and job.minute !=minute:
                job.minute=minute
            if function_name and job.function_name!=function_name:
                job.function_name = function_name
            if parameters and job.parameters != parameters:
                job.parameters = parameters
            if interval and job.interval != interval:
                job.interval = interval
            if interval_unit and job.interval_unit != interval_unit:
                job.interval_unit = interval_unit
        else:
            job = Job(
                name= name,
                trigger=trigger,
                hour=hour,
                minute=minute,
                function_name=function_name,
                parameters=json.dumps(parameters),
                interval=interval,
                interval_unit=interval_unit,
                groups=groups
            )

        db.session.add(job)
        db.session.commit()
        # Schedule the new job
        schedule_job(
            job.id,
            job.function_name,
            job.parameters,
            job.hour,
            job.minute,
            job.interval,
            job.interval_unit
        )

def addJobByDB():
    groups = getDataDictionaryByValue("GROUP_HOSTNAME", socket.gethostname())
    with app.app_context():
        jobs = Job.query.filter_by(groups=groups.code).all()
        for job in jobs:
            schedule_job(
                job.id,
                job.function_name,
                job.parameters,
                job.hour,
                job.minute,
                job.interval,
                job.interval_unit
            )
