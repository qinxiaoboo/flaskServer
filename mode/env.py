from enum import Enum

from flaskServer.config.connect import db

class Env(db.Model):
    __tablename__  = "t_env"

    id = db.Column(db.Integer, primary_key=True)
    t_proxy_id = db.Column(db.Integer, unique=False, nullable=True)
    tw_id = db.Column(db.Integer, unique=True, nullable=True)
    discord_id = db.Column(db.Integer, unique=True, nullable=True)
    outlook_id = db.Column(db.Integer, unique=True, nullable=True)
    okx_id = db.Column(db.Integer, unique=True, nullable=True)
    init_id = db.Column(db.Integer, unique=True, nullable=True)
    bitlight_id = db.Column(db.Integer, unique=True, nullable=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    group = db.Column(db.String(120), unique=False, nullable=True)
    port = db.Column(db.String(120), unique=True, nullable=False)
    cookies = db.Column(db.String(120), unique=False, nullable=True)
    user_agent = db.Column(db.String(80), unique=False, nullable=False)
    # 浏览器状态0:什么都没做，1：初始化了配置，2：初始化了账号和钱包
    status = db.Column(db.Integer, unique=False, nullable=True)
    label = db.Column(db.String(255), unique=False, nullable=True)
    isOpen = db.Column(db.Integer, unique=False, nullable=True)


    def to_json(self):
        return {
            'id':self.id,
            'name':self.name,
            'group':self.group,
            'port':self.port
        }


class InitializationStatus(Enum):
    UNINITIALIZED = 0
    CONFIGURED = 1
    ACCOUNT_INITIALIZED = 2

# 定义一个字典用于映射
status_descriptions = {
    InitializationStatus.UNINITIALIZED.value: "未初始化",
    InitializationStatus.CONFIGURED.value: "初始化配置",
    InitializationStatus.ACCOUNT_INITIALIZED.value: "初始化账号"
}
