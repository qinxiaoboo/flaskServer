from flaskServer.mode.proxy import Proxy
from flaskServer.config.connect import db,app
from sqlalchemy import and_

def getProxyByIp(ip):
    with app.app_context():
        proxy = Proxy.query.filter_by(ip=ip).first()
        return proxy

def update(ip,port,user,pwd):
    proxy = getProxyByIp(ip)
    if proxy:
        return proxy
    else:
        with app.app_context():
            proxy = Proxy(ip=ip,port=port,user=user,pwd=pwd)
            db.session.add(proxy)
            db.session.commit()
            return proxy