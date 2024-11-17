import copy
from my_token import Token
from ast_node import Node
from lexer import Lexer
from parser import Parser
from constants import IDENTIFIER ,ABSTRACTION,APPLICATION
global alpha_reduction_counter
global substitution_counter  

alpha_reduction_counter=0
substitution_counter =  1 
[ print_flag, weak_lambda_calculus_flag ] = [ True, False ];
class Interpreter(object):
    def __init__(self,term):
        self.original_AST=self.clone(term)
        self.term=term
    def clone(self,item):
        return copy.deepcopy(item)
    def terminal_print(self,term):
        print(term)
    def stringify_tree(self,node):
        if(node is None):
            return
        stack=[[node.type,node]]
        str_list=[]
        while(len(stack)):
            [type,obj]=stack.pop()
            if(obj != None and obj.highlight):
                stack.append(['HIGHLIGHT',None])
                str_list.append("[[;#42f5b0;black]")
            if(type == IDENTIFIER):
                #A bit different
                str_list.append(obj.left)
            elif(type == ABSTRACTION):
                str_list.append("(λ")
                stack.append(['CLOSE',None])
                stack.append([obj.right.type,obj.right])
                stack.append(['DOT',None])
                stack.append([obj.left.type,obj.left])
            elif(type == APPLICATION):
                stack.append([obj.right.type,obj.right])
                stack.append([obj.left.type,obj.left])
            elif(type == 'CLOSE'):
                str_list.append(")")
            elif(type == 'DOT'):
                str_list.append(".")
            elif(type == 'HIGHLIGHT'):
                str_list.append("]")
        return ''.join(str_list)
            
            

    def highlight_substitution(self,term,directions):
        return_obj = self.clone(self.original_AST)
        highlight_obj=self.clone(self.original_AST)
        return_root=return_obj
        highlight_root=highlight_obj
        if(len(directions) == 0):
            highlight_obj.left.left.highlight=True
            highlight_obj.right.highlight=True
            return [highlight_obj,term]
        final_dir =directions.pop()
        for index,dir in enumerate(directions):
            if(directions[index] == 'L'):
                return_obj=return_obj.left
                highlight_obj =highlight_obj.left
            elif(directions[index] == 'R'):
                return_obj=return_obj.right
                highlight_obj = highlight_obj.right
        if(final_dir == 'L'):
            highlight_obj.left.left.left.highlight=True
            highlight_obj.left.right.highlight=True
            return_obj.left=term
        elif(final_dir == 'R'):
            highlight_obj.right.left.left.highlight=True
            highlight_obj.right.right.highlight=True
            return_obj.right=term

        return [highlight_root,return_root]
    
            
        

    def is_free_variable(self,term,parameter):
        if(term is None or parameter is None):
            return False
        if(parameter.type != IDENTIFIER):
            return False
        stack=[term]
        while(len(stack)):
            curr=stack.pop(0)
            if(isinstance(curr,str)):
                return False
            if(curr.type ==ABSTRACTION and curr.left.left == parameter.left):
                continue
            if(curr.type == IDENTIFIER and curr.left == parameter.left):
                return True
            if(curr.left != None):
                stack.append(curr.left)
            if(curr.right != None):
                stack.append(curr.right)
        return False


    def substitute(self,expr_body,parameter,substitute_expr):
        alpha_reduction_counter=1
        substitution_counter =1 
        term=expr_body.right
        if(term is None or parameter is None or substitute_expr is None):
            return
        prev=[]
        stack=[]
        stack.append(['RETURN',None,None,None])
        stack.append([term.type,term,parameter,substitute_expr])
        while(len(stack)):
            [type,curr_term,curr_parameter,curr_expression]= stack.pop()
            if(type == IDENTIFIER):
                if(curr_term.left == curr_parameter.left):
                    stack.append(['PREV',curr_expression,None,None])
                else:
                    stack.append(['PREV',curr_term,None,None])
            elif(type == APPLICATION):
                stack.append(['PREV',curr_term,None,None])
                stack.append(['VARIABLE_R',curr_term,None,None])
                stack.append([curr_term.right.type,curr_term.right,curr_parameter,curr_expression])
                stack.append(['VARIABLE_L',curr_term,None,None])
                stack.append([curr_term.left.type,curr_term.left,curr_parameter,curr_expression])
            elif(type == ABSTRACTION):
                if(curr_term.left.left == curr_parameter.left):
                    stack.append(['PREV',curr_term,None,None])
                elif(weak_lambda_calculus_flag or not self.is_free_variable(curr_expression,curr_term.left)):
                    stack.append(['PREV',curr_term,None,None])
                    stack.append(['VARIABLE_R',curr_term,None,None])
                    stack.append([curr_term.right.type,curr_term.right,curr_parameter,curr_expression])
                else:
                    stack.append(['RETURN_ALPHA',None,None,None])
                    stack.append(['PREV',expr_body,None,None])
                    stack.append(['UPDATE',curr_term,curr_parameter,curr_expression])
                    stack.append(['VARIABLE_R',curr_term,None,None])
                    stack.append([curr_term.right.type,curr_term.right,curr_term.left,Node(IDENTIFIER,'[S_' + str(alpha_reduction_counter) + ']',None)])
            elif(type == 'VARIABLE_L'):
                curr_term.left=prev.pop()
            elif(type == 'VARIABLE_R'):
                curr_term.right=prev.pop()
            elif(type == 'RETURN'):
                if(print_flag):
                    self.terminal_print('BETA REDUCTION (' + str(substitution_counter) + '):')
                    substitution_counter += 1
                return prev.pop()
            elif(type == 'RETURN_ALPHA'):
                if(print_flag):
                    self.terminal_print('ALPHA CONVERSION (' + str(substitution_counter) + '):')
                    substitution_counter += 1
                return Node(APPLICATION,prev.pop(),substitute_expr)
            elif(type == 'PREV'):
                prev.append(curr_term)
            elif(type == 'UPDATE'):
                curr_term.left.left = '[S_' + str(alpha_reduction_counter) + ']'
                alpha_reduction_counter += 1

    def interpret(self):
        if(self.term is None):
            return
        prev=[]
        stack=[]
        prev_direction=[]
        stack.append(['RETURN',None,None])
        stack.append([self.term.type,self.term,[]])
        
        while(len(stack)):
            '''
            for x in stack:
                for i in x:
                    print(i)
                print()'''    
            [type,obj,direction] = stack.pop()

            if(type == ABSTRACTION):
                if(not weak_lambda_calculus_flag):
                    stack.append(['VARIABLE_R',obj,None])
                    stack.append([obj.right.type,obj.right,direction + ['R']])
            elif(type == APPLICATION):
                stack.append(['COMPUTE',None,direction])
                stack.append([obj.right.type,self.clone(obj.right),direction + ['R']])
                stack.append([obj.left.type,self.clone(obj.left),direction + ['L']])
            elif(type == 'VARIABLE_R'):
                obj.right=prev.pop()
            elif(type == 'COMPUTE'):
                #raise Exception("TODO !")
                right_redex=prev.pop()
                left_redex=prev.pop()
                prev.pop()
                if(left_redex.type == ABSTRACTION):
                    #print(right_redex ,"I HAVE AN IDENTIFIER")
                    term=self.substitute(left_redex,left_redex.left,right_redex)
                    stack.append([term.type,term,prev_direction + direction])
                    if(print_flag):
                        if(not isinstance(term ,str)):
                            continue
                    [highlight_root,return_root] =self.highlight_substitution(term,direction)
                    self.terminal_print(stringify_tree(highlight_root) + ' ---->' + stringify_tree(return_root))
                    self.original_AST=return_root
                else:
                    prev.append(Node(APPLICATION,left_redex,right_redex))
            elif(type == 'RETURN'):
                return prev.pop()
            if(type == IDENTIFIER or type == ABSTRACTION or type == APPLICATION):
                prev.append(obj)
        return prev.pop()        
