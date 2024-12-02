class Machine(object):
    def __init__(self,ruleset,tape,head):
        self.ruleset=ruleset
        self.tape=tape
        self.head=head
        self.running=False
    def get_status(self):
        head_state, head_location = self.head.getStatus()
        return [
            f"CURRENT STATE: {head_state}",
            self.tape.get_status() , "<br>" , "&#8200;" * (int(head_location) * 6) , "^"
        ]    
    def shift_head(self,move):
        if(self.head.location == 0 and move == "L"):
            self.tape.extend_left()
        elif(self.head.location == ((len(self.tape.tape)-1)) and move == "R"):
            self.tape.extend_right()
            self.head.location += 1
        elif(move == "L"):
            self.head.location -= 1
        elif(move == "R"):
            self.head.location += 1

    def step_lookup(self):
        try:
            if (self.ruleset[self.head.state] and
            self.ruleset[self.head.state][self.tape.tape[self.head.location]]):
                output = self.ruleset[self.head.state][self.tape.tape[self.head.location]]
            
            if (output[0] == self.head.state and output[1] == self.tape.tape[self.head.location] and
                not (output[2] == "L" or output[2] == "R")):
                return False
            
            return output
        except KeyError:
            
            return False

    def get_state(self):
        return {
            'tape':self.tape.tape,
            'head_position':self.head.location,
            'current_state':self.head.state
        }
    def new_step(self):
        if self.step_lookup():
            super().new_step()
            return self.get_state()
        return None
    def step(self):
        
        rule_set=self.step_lookup()
        if(isinstance(rule_set,bool)):
           return 
        new_state=rule_set[0]
        new_symbol=rule_set[1]
        new_move=rule_set[2]
        self.tape.write(new_symbol,self.head.location)
        self.head.state=new_state
        self.shift_head(new_move)
    def run(self):
        self.running=True
        states=[]
        states.append(self.get_state())
        while(self.step_lookup()):
            self.step()
            states.append(self.get_state())
        
            #self.get_status()
        #return self.tape.tape
        return states
            
            
        
