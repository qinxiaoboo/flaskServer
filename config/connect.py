import time

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask import Flask
# 数据库配置
HostName = "localhost"
Port = 3306  # 默认为3306，需要自行修改
UserName = "root"  # 默认用户名
Password = ""
DataBase = "web"
app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{UserName}:{Password}@{HostName}:{Port}/{DataBase}?charset=utf8mb4"

# 配置连接池的参数
app.config['SQLALCHEMY_POOL_SIZE'] = 20  # 最大连接池大小
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 30  # 超时时间，单位秒
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 30  # 最多溢出20个连接

# 是否显示底层执行的SQL语句
# app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)  # 创建db对象

# with app.app_context():
#     db.create_all()
# # ----测试连接是否成功----#
# with app.app_context():  # 解决上下文问题
#     with db.engine.connect() as conn:
#         rs = conn.execute(text("select 1"))
#         print(rs.fetchone())

if __name__ == '__main__':
    app.run(use_reloader=False)