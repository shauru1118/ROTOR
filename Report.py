class Report:
    def __init__(self, user_login: str, routes: int, passengers: int,
                 fuel_bonus, *, id: int | None = None):
        self.user_login = user_login
        self.routes = routes
        self.passengers = passengers
        self.fuel_bonus = fuel_bonus
    
    @staticmethod
    def to_report(data: list | tuple | dict):
        if type(data) in [list, tuple]:
            if len(data) > 3:
                return Report(data[1], data[2], data[3], data[4], id=data[0])
            return Report(data[0], data[1], data[2], data[3])
        if type(data) == dict:
            return Report(data["user_login"], data["routes"], 
                        data["passengers"], data["fuel_bonus"])
    
    def to_dict(self):
        return {
            "routes": self.routes,
            "passengers": self.passengers,
            "fuel_bonus": self.fuel_bonus
        }