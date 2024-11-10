class Head(object):
    def __init__(self,state,location):
        self.state=state
        self.location=int(location)
    def getStatus(self):
        return [self.state,self.location]
    def update(self,state,location):
        self.state=state
        self.location= int(location)
    def display_info(self):
        print(f"The state is {self.state} and location {self.location}")


