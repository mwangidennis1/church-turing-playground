
#represents a token
class Token(object):
    def __init__(self,type,value):
        self.type =type
        self.value=value
    def print_token(self):
        print(f"The token has this type and value {self.type}  {self.value}");

#representing a node
class Node(object):
    def __init__(self,type,left,right):
        self.type=type
        self.left=left
        self.right=right
        self.highlight=False

    def print_node(self):
        print(f"This is the state of the node: {self.left} {self.type} {self.right}");

#method to transform strings into arrays of unique element
#TODO ! Lexographical ordering
def get_input_alphabet(string):
    if(len(string)):
        input_alphabet=set()
        for x in string:
            input_alphabet.add(x)
        return list(input_alphabet)
    return []
#p= get_input_alphabet("okiedokie");
#print(p)
