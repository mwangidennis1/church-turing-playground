import re
import copy
#for testing
weak_lambda_calculus_flag=False
print_flag=True
IDENTIFIER = 101;
ABSTRACTION= 102;
APPLICATION=103;
class Token(object):
    def __init__(self,type,value):
        self.type=type
        self.value=value
class Node(object):
    def __init__(self,type,left,right):
        self.type=type
        self.left=left
        self.right=right
        self.highlight=False
def clone(item):
    return copy.deepcopy(item)

def stringify_tree(node):
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
            
            
def terminal_print(term):
    print(term)
def parser(command):
    #token
    index=0
    #token_list
    parser_list=[]
    internal_flag=False
    res=[char for char in command]

    while(index < len(res)):
        element = res[index]
        if(element == 'I' ):#I = (\x.x)
            token_list=[Token(ord('('),'('),
                        Token(ord('\\'),'\\'),
                        Token(IDENTIFIER,'x'),
                        Token(ord('.'),'.'),
                        Token(IDENTIFIER,'x'),
                        Token(ord(')'),')'),
                        ]
            parser_list.extend(token_list)
        elif(element == 'S'):#S = (\xyz.xz(yz))
            token_list=[Token(ord('('),'('),
                        Token(ord('\\'),'\\'),
                        Token(IDENTIFIER,'x'),
                        Token(IDENTIFIER,'y'),
                        Token(IDENTIFIER,'z'),
                        Token(ord('.'),'.'),
                        Token(IDENTIFIER,'x'),
                        Token(IDENTIFIER,'z'),
                        Token(ord('('),'('),
                        Token(IDENTIFIER,'y'),
                        Token(IDENTIFIER,'z'),
                        Token(ord(')'),')'),
                        Token(ord(')'),')'),
                        ]
            
            parser_list.extend(token_list)
        elif(element == 'K'):# (\x.\y.x) have not represented to spec
            token_list=[Token(ord('('),'('),
                        Token(ord('\\'),'\\'),
                        Token(IDENTIFIER,'x'),
                        Token(IDENTIFIER,'y'),
                        Token(ord('.'),'.'),
                        Token(IDENTIFIER,'x'),
                        Token(ord(')'),')'),
                        ]
            parser_list.extend(token_list)
        elif(element == 'B'):#composition (\xyz.x(yz))
            token_list=[Token(ord('('),'('),
                        Token(ord('\\'),'\\'),
                        Token(IDENTIFIER,'x'),
                        Token(IDENTIFIER,'y'),
                        Token(IDENTIFIER,'z'),
                        Token(ord('.'),'.'),
                        Token(IDENTIFIER,'x'),
                        Token(ord('('),'('),
                        Token(IDENTIFIER,'y'),
                        Token(IDENTIFIER,'z'),
                        Token(ord(')'),')'),
                        Token(ord(')'),')'),
                        ]
            parser_list.extend(token_list)
        elif(element == 'C'):#rep flip function (\xyz.xzy)
            token_list=[Token(ord('('),'('),
                        Token(ord('\\'),'\\'),
                        Token(IDENTIFIER,'x'),
                        Token(IDENTIFIER,'y'),
                        Token(IDENTIFIER,'z'),
                        Token(ord('.'),'.'),
                        Token(IDENTIFIER,'x'),
                        Token(IDENTIFIER,'z'),
                        Token(IDENTIFIER,'y'),
                        Token(ord(')'),')'),
                        ]
            parser_list.extend(token_list)
        elif(element == 'W'): #duplication (\xy.x yy)
            token_list=[Token(ord('('),'('),
                        Token(ord('\\'),'\\'),
                        Token(IDENTIFIER,'x'),
                        Token(IDENTIFIER,'y'),
                        Token(ord('.'),'.'),
                        Token(IDENTIFIER,'x'),
                        Token(IDENTIFIER,'y'),
                        Token(IDENTIFIER,'y'),
                        Token(ord(')'),')'),
                        ]
            parser_list.extend(token_list)
        elif(element == 'M'): #mocking combinator(a function applied to iself) (\f.ff)
            token_list=[Token(ord('('),'('),
                        Token(ord('\\'),'\\'),
                        Token(IDENTIFIER,'f'),
                        Token(ord('.'),'.'),
                        Token(IDENTIFIER,'f'),
                        Token(IDENTIFIER,'f'),
                        Token(ord(')'),')'),
                        ]
            parser_list.extend(token_list)
        elif(element == 'H'):
            token_list=[Token(ord('('), '('),
	       		Token(ord('\\'), '\\'),
			Token(IDENTIFIER, 'f'),
			Token(ord('.'), '.'),
		        Token(IDENTIFIER, 'f'),
			Token(ord('('), '('), 
		        Token(ord('\\'), '\\'),
		        Token(IDENTIFIER, 'z'),
		        Token(ord('.'), '.'),
		        Token(ord('('), '('), 
			Token(ord('\\'), '\\'),
			Token(IDENTIFIER, 'x'),
			Token(ord('.'), '.'),
			Token(ord('('), '('), 
			Token(ord('\\'), '\\'),
			Token(IDENTIFIER, 'f'),
			Token(ord('.'), '.'),
			Token(IDENTIFIER, 'f'),
			Token(ord('('), '('), 
			Token(ord('\\'), '\\'),
			Token(IDENTIFIER, 'z'),
			Token(ord('.'), '.'),
			Token(IDENTIFIER, 'x'),
			Token(IDENTIFIER, 'x'),
			Token(IDENTIFIER, 'f'),
			Token(IDENTIFIER, 'z'),
			Token(ord(')'), ')'),
			Token(ord(')'), ')'),
			Token(ord(')'), ')'),
			Token(ord('('), '('), 
			Token(ord('\\'), '\\'),
			Token(IDENTIFIER, 'x'),
			Token(ord('.'), '.'),
			Token(ord('('), '('), 
			Token(ord('\\'), '\\'),
			Token(IDENTIFIER, 'f'),
			Token(ord('.'), '.'),
			Token(IDENTIFIER, 'f'),
			Token(ord('.'), '('), 
			Token(ord('\\'), '\\'),
			Token(IDENTIFIER, 'z'),
			Token(ord('.'), '.'),
			Token(IDENTIFIER, 'x'),
			Token(IDENTIFIER, 'x'),
			Token(IDENTIFIER, 'f'),
			Token(IDENTIFIER, 'z'),
			Token(ord(')'), ')'),
			Token(ord(')'), ')'),
			Token(ord(')'), ')'),
			Token(IDENTIFIER, 'f'),
			Token(IDENTIFIER, 'z'),	
			Token(ord(')'), ')'),
			Token(ord(')'), ')'),
	                ]
            parser_list.extend(token_list)
        elif(re.match(r'[a-zA-Z]',element)):
             token=Token(IDENTIFIER,element)
             parser_list.append(token)           
        elif(element == 'λ' or element == '\\'):
            token=Token(ord('\\'),element)
            parser_list.append(token)
        elif(element == '.'):
            token=Token(ord('.'),element)
            parser_list.append(token)
        elif(element == '('):
            token=Token(ord('('),element)
            parser_list.append(token)
        elif(element == ')'):
            token=Token(ord(')'),element)
            parser_list.append(token)
        elif(element == '['):
            token=Token(ord('['),'\\[')
            parser_list.append(token)
            internal_flag=True
        elif(element == ']'):
            token=Token(ord(']'),'\\]')
            parser_list.append(token)
            internal_flag=False
        else:
            if(internal_flag == True):
                token=Token(IDENTIFIER,element)
                parser_list.append(token)
        index += 1
    return parser_list
    #print([i.value for i in parser_list])
#token_list=[Token(ord('('), '(')]
#interface methods for parser

def skip_type(type):
    if(next_type(type)):
        token_list.pop(0)
        return True
    return False
def match_type(type):
    if(next_type(type)):
        token_list.pop(0)
        return
    raise Exception(f"Something went badly wrong! (INCORRECT MATCH WITH TYPE: {type} )")
def next_type(type):
    if(len(token_list) == 0 or token_list is None):
        return None
    return token_list[0].type == type
'''functions which the parser will use to build our
   AST which will have nodes representing our alternatives
   to the production rules eg IDENTIFIER,ABSTRACTION &
   APPLICATION '''
def expression():
    if(skip_type(ord('\\'))):
       
       parameter=None
       if(next_type(IDENTIFIER)):
          parameter=Node(IDENTIFIER,token_list.pop(0).value,None)
       elif(skip_type(ord('['))):
          internal_name=''
          while(not skip_type(ord(']'))):
                internal_name= internal_name + token_list.pop(0).value
          parameter=Node(IDENTIFIER,'[' + internal_name + ']',None)
       else:
          raise Exception("The parameter in lambda abstraction is not correct (PARAMETER NOT IDENTIFIER 326)")
       if(not skip_type(ord('.'))):
          if(next_type(IDENTIFIER)):
             token_list.insert(0,Token(ord('\\'),'\\'))
          else:
             raise Exception("The parameter in lambda abstraction is not correct (PARAMETER NOT IDENTIFIER 326)")
       expr=expression()
       return Node(ABSTRACTION,parameter,expr)

    return application()

def application():
    left_child=atom()
    while(True):
        right_child=atom()
        if(left_child is None or right_child is None):
            return left_child
        left_child=Node(APPLICATION,left_child,right_child)
        
def atom():
    if(skip_type(ord('('))):
        expr=expression()
        match_type(ord(')'))
        if(expr is  None):
            return expression()
        return expr
    elif(skip_type(ord('['))):
        internal_name=''
        while(not skip_type(ord(']'))):
            internal_name= internal_name + token_list.pop(0).value
        return Node(IDENTIFIER,'[' + internal_name + ']',None)
    elif(next_type(ord('\\'))):
        return expression()
    elif(next_type(IDENTIFIER)):
        return Node(IDENTIFIER,token_list.pop(0).value,None)
    return None
'''to avoid vaiable colisions'''
def convert_to_T_Brujin(node):
    if(node is None):
        return
    stack=[]
    output=''
    stack.append(['RETURN',node,None])
    stack.append([node.type,node,{}])
    while(len(stack)):
        [type,curr_node,context] = stack.pop()
        if(type == IDENTIFIER):
            if(curr_node.left in context):
                output +='> ' + str(context[curr_node.left]) + ' '
            else:
                output += '> '
        elif(type == ABSTRACTION):
            for key,value in context.items():
                context[key] += 1
            context[curr_node.left.left]=0
            output +='λ '
            stack.append([curr_node.right.type,curr_node.right,context])
        elif(type == APPLICATION):
            output +='@ '
            stack.append([curr_node.right.type,curr_node.right,clone(context)])
            stack.append([curr_node.left.type,curr_node.left,clone(context)])
        elif(type == 'RETURN'):
            return output
        else:
            raise Exception("Something happened when de brujining")

def is_free_variable(term,parameter):
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

def highlight_substitution(term,directions):
    return_obj = clone(original_AST)
    highlight_obj=clone(original_AST)
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
    
            
        
def substitute(expr_body,parameter,substitute_expr):
    global substitution_counter
    global alpha_reduction_counter
    substitution_counter=1
    alpha_reduction_counter=1
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
            elif(weak_lambda_calculus_flag or not is_free_variable(curr_expression,curr_term.left)):
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
                terminal_print('BETA REDUCTION (' + str(substitution_counter) + '):')
                substitution_counter += 1
            return prev.pop()
        elif(type == 'RETURN_ALPHA'):
            if(print_flag):
                terminal_print('ALPHA CONVERSION (' + str(substitution_counter) + '):')
                substitution_counter += 1
            return Node(APPLICATION,prev.pop(),substitute_expr)
        elif(type == 'PREV'):
            prev.append(curr_term)
        elif(type == 'UPDATE'):
            curr_term.left.left = '[S_' + str(alpha_reduction_counter) + ']'
            alpha_reduction_counter += 1
        
            

def interpret(term):
    if(term is None):
        return
    prev=[]
    stack=[]
    prev_direction=[]
    stack.append(['RETURN',None,None])
    stack.append([term.type,term,[]])
    while(len(stack)):
        for x in stack:
            for i in x:
                print(i)
            print()    
        [type,obj,direction] = stack.pop()

        if(type == ABSTRACTION):
            if(not weak_lambda_calculus_flag):
                stack.append(['VARIABLE_R',obj,None])
                stack.append([obj.right.type,obj.right,direction + ['R']])
        elif(type == APPLICATION):
            stack.append(['COMPUTE',None,direction])
            stack.append([obj.right.type,clone(obj.right),direction + ['R']])
            stack.append([obj.left.type,clone(obj.left),direction + ['L']])
        elif(type == 'VARIABLE_R'):
            obj.right=prev.pop()
        elif(type == 'COMPUTE'):
            #raise Exception("TODO !")
            
            right_redex=prev.pop()
            left_redex=prev.pop()
            prev.pop()
            if(left_redex.type == ABSTRACTION):
                #print(right_redex ,"I HAVE AN IDENTIFIER")
                term=substitute(left_redex,left_redex.left,right_redex)
                stack.append([term.type,term,prev_direction + direction])
                if(print_flag):
                    if(not isinstance(term ,str)):
                        continue
                    #pass
                    [highlight_root,return_root] =highlight_substitution(term,direction)
                    original_AST=return_root
            else:
                prev.append(Node(APPLICATION,left_redex,right_redex))
        elif(type == 'RETURN'):
            return prev.pop()
        if(type == IDENTIFIER or type == ABSTRACTION or type == APPLICATION):
            prev.append(obj)
    return prev.pop()        




token_list=parser('(λx.x)(λy.y)')
print([i.value for i in token_list])
AST=expression()
if(AST is None):
    raise Exception("An unexpected error occured")

original_AST=clone(AST)
print(original_AST.right.type)
print(original_AST.left.right.type)
print(original_AST.left.right.left)
print(original_AST.left.right.right)
'''de_output=convert_to_T_Brujin(AST)
print(de_output)
reduced_ast=interpret(AST)
print("**********************************")
print(reduced_ast)
red=stringify_tree(reduced_ast)
print(red)'''
