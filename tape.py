class Tape(object):
    def __init__(self,tape):
        if tape is None:
            self.tape=[]
        else:
            self.tape=tape
    def get_status(self):
        return self.tape
    def extend_left(self):
        self.tape.insert(0,"B")
    def extend_right(self):
        self.tape.append("B")
    def write(self,symbol,location):
        self.tape[location]=symbol
    def display_info(self):
         print(f"The tape values are: {self.tape}")


