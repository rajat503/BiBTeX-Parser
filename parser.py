import ply.lex as lex
import ply.yacc as yacc

import MySQLdb
db = MySQLdb.connect("localhost","root","root","BibTex")
cursor = db.cursor()

records={}
records['bibkey']="NULL"
records['bibtype']="NULL"
records['address']="NULL"
records['author']="NULL"
records['booktitle']="NULL"
records['chapter']="NULL"
records['edition']="NULL"
records['journal']="NULL"
records['number']="NULL"
records['pages']="NULL"
records['publisher']="NULL"
records['school']="NULL"
records['title']="NULL"
records['volume']="NULL"
records['year']="NULL"

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
t_STRING = r'{[^{}]+}'
t_ignore=' \t\n\v\r'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def p_bibfile(p):
    'bibfile : entries'
    p[0] = p[1]

def p_entries(p):
    '''entries : entry entries
               | entry'''
    if len(p) > 2:
        p[0] = p[1]+p[2]
    else:
        p[0] = p[1]

def p_entry(p):
    'entry : AT NAME LBRACE key COMMA fields RBRACE'
    p[0]=p[1]+p[2]+p[3]+p[4]+p[5]+p[6]+p[7]
    records['bibkey']=p[4]
    records['bibtype']=p[2]

    #insert to db
    print records
    sql = "INSERT INTO entries(bibkey, bibtype, address, author, booktitle, chapter, edition, journal, number, pages, publisher, school, title, volume, year) \
           VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" % \
           (records['bibkey'], records['bibtype'], records['address'], records['author'],records['booktitle'],records['chapter'],records['edition'],records['journal'],records['number'],records['pages'],records['publisher'],records['school'],records['title'],records['volume'],records['year'])

    cursor.execute(sql)
    db.commit()

    for i in records.keys():
        records[i]='NULL'


def p_key(p):
    '''key : NAME
           | NUMBER'''
    p[0] = p[1]

def p_fields(p):
    '''fields : field COMMA fields
              | field'''

    if len(p)>2:
        p[0] = p[1]+p[2]+p[3]
    else:
        p[0] = p[1]

def p_field(p):
    'field : NAME EQUALS LBRACE value RBRACE'
    p[0] = p[1]+p[2]+p[3]+p[4]+p[5]
    records[p[1]]=p[4]

def p_value(p):
    '''value : STRING
             | NUMBER
             | NAME'''
    p[0] = p[1]

data = '''@article{key1,
author = {{Sarkar, Santonu}},
title = {{John Smith}}}
@book{ourbook,
author = {{joe smith and john Kurt}},
title = {{Our Little Book}},
year = {{1997}}
}
'''

lexer = lex.lex()
lexer.input(data)

# while True:
#     tok = lexer.token()
#     if not tok:
#         break      # No more input
#     print(tok)

parser = yacc.yacc()
parser.parse(data)

db.close()
