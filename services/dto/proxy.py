from flaskServer.mode.proxy import Proxy
from flaskServer.config.connect import db,app
from sqlalchemy import and_

def getProxyByIp(ip):
    with app.app_context():
        proxy = Proxy.query.filter_by(ip=ip).first()
        return proxy
def getProxyByID(_id):
    with app.app_context():
        proxy = Proxy.query.filter_by(id=_id).first()
        return proxy

def update(ip,port,user,pwd):
    proxy = getProxyByIp(ip)
    with app.app_context():
        if proxy:
            if proxy.port != port:
                proxy.port = port
            if proxy.user != user:
                proxy.user = user
            if proxy.pwd != pwd:
                proxy.pwd = pwd
        else:
            proxy = Proxy(ip=ip,port=port,user=user,pwd=pwd)
        db.session.add(proxy)
        db.session.commit()
        print("新增一条代理信息，id：",proxy.id)
        return proxy

if __name__ == '__main__':
    update("168.80.24.58","8099","oz2USP43","Pr382u")