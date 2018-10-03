
class User:

    def __init__(self,name,password,role):
        self.name = name
        self.password = password
        self.role = role


class Order:

    def __init__(self,food):
        self.food = food  
        self.status = "Incomplete"      