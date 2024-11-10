from token import Token
from ast_node import Node
from lexer import Lexer
from constants import IDENTIFIER ,ABSTRACTION,APPLICATION 
 

class Parser(object):
    def __init__(self,token_list):
        if token_list is None:
            raise Exception("Parser needs a token list")
        self.token_list =token_list
    def skip_type(self,type):
        if(self.next_type(type)):
            self.token_list.pop(0)
            return True
        return False
    def match_type(self,type):
        if(self.next_type(type)):
            self.token_list.pop(0)
            return
        raise Exception(f"Something went badly wrong! (INCORRECT MATCH WITH TYPE: {type} )")
    def next_type(self,type):
        if(len(self.token_list) == 0 or self.token_list is None):
            return None
        return self.token_list[0].type == type
    def expression(self):
        if(self.skip_type(ord('\\'))):
            parameter=None
            if(self.next_type(IDENTIFIER)):
                parameter=Node(IDENTIFIER,self.token_list.pop(0).value,None)
            elif(self.skip_type(ord('['))):
                internal_name=''
                while(not self.skip_type(ord(']'))):
                    internal_name= internal_name + self.token_list.pop(0).value
                parameter=Node(IDENTIFIER,'[' + internal_name + ']',None)
            else:
                raise Exception("The parameter in lambda abstraction is not correct (PARAMETER NOT IDENTIFIER 326)")
            if(not self.skip_type(ord('.'))):
                if(self.next_type(IDENTIFIER)):
                    self.token_list.insert(0,Token(ord('\\'),'\\'))
                else:
                    raise Exception("The parameter in lambda abstraction is not correct (PARAMETER NOT IDENTIFIER 326)")
            expr=self.expression()
            return Node(ABSTRACTION,parameter,expr)

        return self.application()

    def application(self):
        left_child=self.atom()
        while(True):
            right_child=self.atom()
            if(left_child is None or right_child is None):
                return left_child
            left_child=Node(APPLICATION,left_child,right_child)
        
    def atom(self):
        if(self.skip_type(ord('('))):
            expr=self.expression()
            self.match_type(ord(')'))
            if(expr is  None):
                return self.expression()
            return expr
        elif(self.skip_type(ord('['))):
            internal_name=''
            while(not self.skip_type(ord(']'))):
                internal_name= internal_name + self.token_list.pop(0).value
            return Node(IDENTIFIER,'[' + internal_name + ']',None)
        elif(self.next_type(ord('\\'))):
            return self.expression()
        elif(self.next_type(IDENTIFIER)):
            return Node(IDENTIFIER,self.token_list.pop(0).value,None)
        return None


