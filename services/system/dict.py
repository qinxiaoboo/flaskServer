from flaskServer.mode.sys_dict import SysDict
from sqlalchemy import and_
from flask import jsonify
import json

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