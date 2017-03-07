import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'AT',
    'NEWLINE',
    'COMMENT',
    'WHITESPACE',
    'JUNK',
    'NUMBER',
    'NAME',
    'LBRACE',
    'RBRACE',
    'LPAREN',
    'RPAREN',
    'EQUALS',
    'HASH',
    'COMMA',
    'QUOTE',
    'STRING'
)

t_AT = r'\@'
t_NEWLINE = r'\n'
t_COMMENT = r'\%~[\n]*\n'
t_WHITESPACE = r'[\ \r\t]+'
t_JUNK = r'~[\@\n\ \r\t]+'
t_NUMBER = r'[0-9]+'
t_NAME = r'[a-zA-Z0-9\!\$\&\*\+\-\.\/\:\;\<\>\?\[\]\^\_\'\|]+'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_HASH = r'\#'
t_COMMA = r','
t_QUOTE = r'\"'
t_STRING = r'{[^{}]}'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)



data = '''
@article{key1,
author = {Sarkar, Santonu},
title = "John Smith"}
@book{ourbook,
author = {joe smith and john Kurt},
title = {Our Little Book},
year = {1997}
}
'''

lexer = lex.lex()
lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
