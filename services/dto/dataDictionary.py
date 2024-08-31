from flaskServer.mode.dataDictionary import DataDictionary
from flaskServer.config.connect import db, app
from sqlalchemy import and_

def getDataDictionaryById(dd_id):
    with app.app_context():
        entry = DataDictionary.query.get(id)
        return entry
def getAll():
    List = []
    with app.app_context():
        entrys = DataDictionary.query.all()
        for entry in entrys:
            List.append(entry.to_dict())
        return List
def getDataDictionaryByName(group,code):
    with app.app_context():
        entry = DataDictionary.query.filter(and_(DataDictionary.code==code,DataDictionary.group_name==group)).first()
        return entry
def getDataDictionaryByValue(group,value):
    with app.app_context():
        entry = DataDictionary.query.filter(and_(DataDictionary.value==value,DataDictionary.group_name==group)).first()
        return entry

def updataDataDictionary(group,code,value,desc):
    entry = getDataDictionaryByName(group,code)
    if entry:
        if entry.value!=value:
            entry.value = value
        if entry.description != desc:
            entry.description = desc
    else:
        entry = DataDictionary(
            group_name=group,
            code=code,
            value=value,
            description=desc
        )
    db.session.add(entry)
    db.session.commit()

def deleteDataDictionary(id):
    entry = DataDictionary.query.get(id)
    if entry:
        db.session.delete(entry)
        db.session.commit()
        return True
    return False