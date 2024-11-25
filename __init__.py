from my_token import Token
from ast_node import Node
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter,printing_stuff
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
        #print('\n' ,result , printing_stuff)
        return result
    except Exception as e:
        print(f"Somthing unexpected happended: {e} ")


@app.route('/machine',methods=['POST'])
def get_machine_state():
    data=request.get_json()
    tape_list=list(data["tape"])
    x,y=data["head"].split(" ")
    rule_list=json.loads(data["rule_set"])
    t1=Tape(tape_list)
    h1=Head( ''.join(x),''.join(y));
    h1.display_info()
    m1=Machine(rule_list,t1,h1);
    #result=m1.run()
    all_states=[]
    all_states.append({
        'tape': list(t1.tape),  # Convert tape to list if it isn't already
        'head_position': h1.location,
        'current_state': h1.state
    })
    while m1.step_lookup():
        m1.step()
        all_states.append({
            'tape': list(t1.tape),
            'head_position': h1.location,
            'current_state': h1.state
        })
    print(all_states)
    return jsonify(all_states)


@app.route('/')
def serve_html():
    return send_file('./static/index.html')

@app.route('/parse_expression',methods=['GET'])
def parse_expression():
    try:
        expression = request.args.get('expression')
        print(str(expression))
        result=evaluate_lambda(str(expression))
        printing_stuff.append(result)
        print(f"Here is the result: {printing_stuff} ")
        return jsonify(printing_stuff)
    finally:
        printing_stuff.clear()
if __name__=="__main__":
    app.run(debug=True)
    
    

    
    
