import re
from token import Token
from constants import IDENTIFIER ,ABSTRACTION,APPLICATION
IDENTIFIER = 101
ABSTRACTION = 102
APPLICATION = 103

class Lexer(object):
    def __init__(self, input_text):
        if input_text is None:
            raise Exception("No lambda strings to be tokenized")
        self.input_text = input_text

    def lexer(self):
        # token
        index = 0
        # token_list
        parser_list = []
        internal_flag = False
        res = [char for char in self.input_text]

        while index < len(res):
            element = res[index]
            if element == 'I':  # I = (\x.x)
                token_list = [
                    Token(ord('('), '('),
                    Token(ord('\\'), '\\'),
                    Token(IDENTIFIER, 'x'),
                    Token(ord('.'), '.'),
                    Token(IDENTIFIER, 'x'),
                    Token(ord(')'), ')')
                ]
                parser_list.extend(token_list)
            elif element == 'S':  # S = (\xyz.xz(yz))
                token_list = [
                    Token(ord('('), '('),
                    Token(ord('\\'), '\\'),
                    Token(IDENTIFIER, 'x'),
                    Token(IDENTIFIER, 'y'),
                    Token(IDENTIFIER, 'z'),
                    Token(ord('.'), '.'),
                    Token(IDENTIFIER, 'x'),
                    Token(IDENTIFIER, 'z'),
                    Token(ord('('), '('),
                    Token(IDENTIFIER, 'y'),
                    Token(IDENTIFIER, 'z'),
                    Token(ord(')'), ')'),
                    Token(ord(')'), ')')
                ]
                parser_list.extend(token_list)
            elif element == 'K':  # (\x.\y.x)
                token_list = [
                    Token(ord('('), '('),
                    Token(ord('\\'), '\\'),
                    Token(IDENTIFIER, 'x'),
                    Token(IDENTIFIER, 'y'),
                    Token(ord('.'), '.'),
                    Token(IDENTIFIER, 'x'),
                    Token(ord(')'), ')')
                ]
                parser_list.extend(token_list)
            elif element == 'B':  # Composition (\xyz.x(yz))
                token_list = [
                    Token(ord('('), '('),
                    Token(ord('\\'), '\\'),
                    Token(IDENTIFIER, 'x'),
                    Token(IDENTIFIER, 'y'),
                    Token(IDENTIFIER, 'z'),
                    Token(ord('.'), '.'),
                    Token(IDENTIFIER, 'x'),
                    Token(ord('('), '('),
                    Token(IDENTIFIER, 'y'),
                    Token(IDENTIFIER, 'z'),
                    Token(ord(')'), ')'),
                    Token(ord(')'), ')')
                ]
                parser_list.extend(token_list)
            elif element == 'C':  # Flip function (\xyz.xzy)
                token_list = [
                    Token(ord('('), '('),
                    Token(ord('\\'), '\\'),
                    Token(IDENTIFIER, 'x'),
                    Token(IDENTIFIER, 'y'),
                    Token(IDENTIFIER, 'z'),
                    Token(ord('.'), '.'),
                    Token(IDENTIFIER, 'x'),
                    Token(IDENTIFIER, 'z'),
                    Token(IDENTIFIER, 'y'),
                    Token(ord(')'), ')')
                ]
                parser_list.extend(token_list)
            elif element == 'W':  # Duplication (\xy.x yy)
                token_list = [
                    Token(ord('('), '('),
                    Token(ord('\\'), '\\'),
                    Token(IDENTIFIER, 'x'),
                    Token(IDENTIFIER, 'y'),
                    Token(ord('.'), '.'),
                    Token(IDENTIFIER, 'x'),
                    Token(IDENTIFIER, 'y'),
                    Token(IDENTIFIER, 'y'),
                    Token(ord(')'), ')')
                ]
                parser_list.extend(token_list)
            elif element == 'M':  # Mocking combinator (\f.ff)
                token_list = [
                    Token(ord('('), '('),
                    Token(ord('\\'), '\\'),
                    Token(IDENTIFIER, 'f'),
                    Token(ord('.'), '.'),
                    Token(IDENTIFIER, 'f'),
                    Token(IDENTIFIER, 'f'),
                    Token(ord(')'), ')')
                ]
                parser_list.extend(token_list)
            elif element == 'H':
                token_list = [
                    Token(ord('('), '('),
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
                    Token(ord(')'), ')')
                ]
                parser_list.extend(token_list)
            elif re.match(r'[a-zA-Z]', element):
                token = Token(IDENTIFIER, element)
                parser_list.append(token)
            elif element == 'λ' or element == '\\':
                token = Token(ord('\\'), element)
                parser_list.append(token)
            elif element == '.':
                token = Token(ord('.'), element)
                parser_list.append(token)
            elif element == '(':
                token = Token(ord('('), element)
                parser_list.append(token)
            elif element == ')':
                token = Token(ord(')'), element)
                parser_list.append(token)
            elif element == '[':
                token = Token(ord('['), '\\[')
                parser_list.append(token)
                internal_flag = True
            elif element == ']':
                token = Token(ord(']'), '\\]')
                parser_list.append(token)
                internal_flag = False
            else:
                if internal_flag:
                    token = Token(IDENTIFIER, element)
                    parser_list.append(token)
            index += 1
        return parser_list
        
'''l=Lexer('(λa. (λb. b a) a) (λz. z) (λw. w) ')
token_list=l.lexer()'''
#print([i.value for i in token_list])
