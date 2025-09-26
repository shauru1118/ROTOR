class User:
    def __init__(self, login, password, vk, account):
        self.login = str(login)
        self.password = str(password)
        self.vk = str(vk)
        self.account = account
        self.total_routes = 0
        self.total_passengers = 0
        self.salary = 0

    def __str__(self):
        return f"{self.login:.<30} {self.password:.<30} {self.vk:.<30} {str(self.account):.<30}"

    def __repr__(self):
        return f"{self.login:.^30} - {self.password:.^30} - {self.vk:.^30} - {str(self.account):.^30}"

    @staticmethod
    def to_user(data):
        if type(data) in [list, tuple]:
            return User(data[0], data[1], data[2], data[3])
        if type(data) == dict:
            return User(data["login"], data["password"], data["vk"], data["account"])

    def to_dict(self):
        return {
            "login": self.login,
            "password": self.password,
            "vk": self.vk,
            "account": self.account
        }

