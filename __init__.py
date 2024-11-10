from token import Token
from ast_node import Node
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from constants import IDENTIFIER ,ABSTRACTION,APPLICATION
def evaluate_lambda(expression):
    try:
        lexer=Lexer(expression)
        token_list=lexer.lexer()
        #print([i.value for i in token_list])
        parser=Parser(token_list)
        original_AST=parser.expression()
        interpreter=Interpreter(original_AST)
        reduced_ast=interpreter.interpret()
        result=interpreter.stringify_tree(reduced_ast)
        print(result)
    except Exception as e:
        print(f"Somthing unexpected happended: {e} ")
def app_run():
    while(True):
        expression=input("Give lambda expresssion")
        evaluate_lambda(expression)
        
        
if __name__=="__main__":
    app_run()
    
    

    
    
