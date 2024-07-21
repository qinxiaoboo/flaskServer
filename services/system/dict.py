from flaskServer.mode.sys_dict import SysDict
from flaskServer.config.connect import db,app
from sqlalchemy import and_


def getInfo(args):
    print(args)
    name = args.get(key="name", default="", type=str)
    key = args.get(key="key", default="", type=str)
    data = []
    query = SysDict.query
    if name:
        query = query.filter(SysDict.name.like('%{}%'.format(name)))
    if key:
        query = query.filter(SysDict.key.like('%{}%'.format(key)))
    result = query.all()
    for item in result:
        data.append(item.to_json())
    print(data)
    return data

def updateInfo(json_data):
    print("insertInfo:",json_data)
    id = json_data.get("id")
    name = json_data.get("name")
    key = json_data.get("key")
    value = json_data.get("value")
    with app.app_context() :
        # 如果id存在则更新
        sysdict = SysDict.query.get(id)
        if sysdict:
            if sysdict.value != value:
                sysdict.value = value
                db.session.commit()
                return sysdict.id
        # 查看数据库有没有重复值,没有则新增
        sysdicts = SysDict.query.filter(and_(SysDict.name==name,SysDict.key==key)).all()
        if len(sysdicts) == 0:
            sysdict = SysDict(name=name, key=key, value=value)
            db.session.add(sysdict)
            db.session.commit()
            return sysdict.id
        return 0

if __name__ == '__main__':
    # sysdict = SysDict(name="KEYS", key="yesCaptcha", value="47b3e9fb8832222e67a900ff6f32c9beef0383e838919")
    # with app.app_context():
    #     db.session.add(sysdict)
    #     db.session.commit()
    #     print(sysdict.id)
    with app.app_context():
        sysdicts = SysDict.query.filter(and_(SysDict.name == "KEYS", SysDict.key == "yesCaptcha")).all()
        print(sysdicts)
