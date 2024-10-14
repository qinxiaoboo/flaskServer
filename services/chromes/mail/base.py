
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

    def getCode(self, text, wtime, num):
        raise NotImplementedError()


