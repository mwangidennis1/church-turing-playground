from my_token import Token
from ast_node import Node
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from constants import IDENTIFIER ,ABSTRACTION,APPLICATION
from flask import Flask,request,jsonify,send_file,render_template,Response
from flask_cors import CORS
from tape import Tape;
from head import Head;
from machine import Machine;
import json
app=Flask(__name__)
CORS(app)
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
        return result
    except Exception as e:
        print(f"Somthing unexpected happended: {e} ")
'''
def app_run():
    while(True):
        expression=input("Give lambda expresssion")
        evaluate_lambda(expression)
'''

@app.route('/machine',methods=['POST'])
def get_machine_state():
    data=request.get_json()
    tape_list=list(data["tape"])
    x,y=data["head"].split(" ")
    rule_list=json.loads(data["rule_set"])
    print(tape_list)
    print(x,y)
    print(rule_list)
    t1=Tape(tape_list)
    h1=Head( ''.join(x),''.join(y));
    h1.display_info()
    m1=Machine(rule_list,t1,h1);
    result=m1.run()
    return result


@app.route('/')
def serve_html():
    return send_file('./static/index.html')

@app.route('/parse_expression',methods=['GET'])
def parse_expression():
    expression = request.args.get('expression')
    print(str(expression))
    result=evaluate_lambda(str(expression))
    print(f"Here is the result: {result} ")
    return Response(result,mimetype='text/plain')
if __name__=="__main__":
    app.run(debug=True)
    
    

    
    
