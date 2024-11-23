
class BaseClient:
    def __init__(self, idx, chrome, envName, username, password):
        self.id = idx
        self.chrome = chrome
        self.tab = None
        self.envName = envName
        self.username = username
        self.password = password

    def login(self):
        raise NotImplementedError()

    def getCode(self, text, wtime=10, num=2, type=None):
        raise NotImplementedError()


