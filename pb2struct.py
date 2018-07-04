# -*- coding: utf-8 -*-
''' Parser foir proto files

Created on 2.7.2018 by tobias badertscher
'''

from ply import yacc
from ply import lex
from ply.lex import TOKEN

class PBLexer:


    keywords = (
        # Module level keywords
        'SYNTAX',
        )
    datatypes = (
        # Data types
        "DOUBLE",
        "FLOAT"
        'UINT64',
        'SINT64',
        'INT64',
        'UINT32',
        'SINT32',
        'INT32',
        "FIXED32",
        "FIXED64",
        "SFIXED32",
        "SFIXED64",
        "BOOL",
        "STRING",
        "BYTES"
        )
    letter = r'[A-Za-z]'
    decimalDigit = r'[0-9]'
    octalDigit = r'[0-7]'
    hexDigit = r'[0-9A-Fa-f]'
    ident = letter + r'(' + letter + '|' + decimalDigit+'|_)*'
    fullIdent = ident +r'(\.' + ident +')*'
    messageName = ident
    enumName = ident
    fieldName = ident
    oneofName = ident
    mapName = ident
    serviceName = ident
    rpcName = ident
    messageType = r'(\.)? ('+ ident +r'\.)*' + messageName
    enumType =  r'(\.)? ('+ ident +r'\.)*' + enumName
    decimalLit = r'[1-9]('+decimalDigit+')*'
    octalLit   = r'0('+ octalDigit +r')*'
    hexLit     = r'0[xX]'+hexDigit+r'('+hexDigit+r')*'
    intLit     = r'(-)?('+decimalLit+r'|'+octalLit+r'|'+hexLit+r')'

    def __init__(self, **kwargs):
        self._lex = lex.lex(module=self, **kwargs)
        self.reserved_map = {}
        for toc in PBLexer.keywords:
            self.reserved_map[toc.lower()]=toc
        for toc in PBLexer.datatypes:
            self.reserved_map[toc.lower()]='DTYPE'
        for toc in PBLexer.keywords:
            self.reserved_map[toc.lower()]='KEYWORD'


    tokens = (
        'DTYPE',
        'EQ',
        'SEMICOLON',
        'LPAREN',
        'RPAREN',
        'LSQBR',
        'RSQBR',
        'LSWBR',
        'RSWBR',
        'NUMBER',
        'IDENTIFIER',
        'STRING',
        'COMMENT',
        'ENUM'
        'MESSAGE'
        )

    t_EQ = r'='
    t_SEMICOLON = r';'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LSQBR = r'\['
    t_RSQBR = r'\]'
    t_LSWBR = r'\{'
    t_RSWBR = r'\}'

    # A regular expression rule with some action code
    @TOKEN(intLit)
    def t_NUMBER(self, t):
        base = 10
        if 'x' in t.value.lower():
            base=16
        elif t.value[0]=='0':
            base = 8
        t.value = int(t.value, base)
        t.base = base
        return t

    def t_STRING(self,t):
        r'\"[a-zA-Z_0-9. ]+\"'
        return t

    @TOKEN(fullIdent)
    def t_IDENTIFIER(self, t):
        t.type = self.reserved_map.get(t.value,"IDENTIFIER")
        return t

    def t_COMMENT(self, t):
        r'/\*(.|\n)*?\*/'
        pass

    def t_COMMENT_ONE_LINE(self, t):
        r'//(.)*'
        pass
        # No return value. Token discarded

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def input(self, data):
        # Give the lexer some input
        self._lex.input(data)

    def token(self):
        return self._lex.token()

class PBParse:

    tokens = PBLexer.tokens

    def __init__(self, **kwargs):
        self._lex = PBLexer()
        self._parser = yacc.yacc(module=self, **kwargs)
        self.line_nr = 0

    def parse(self, data):
        res = self._parser.parse(data, lexer = self._lex)
        return res

    def p_module(self, p):
        '''module  : module enum
                   | module message
                   | empty '''
        print("module " , p)
        print("enum" , p)

    def p_message(self, p):
        ''' message : MESSAGE IDENTIFER  LSWBR definition_list RSWBR'''
        print("message" , p)

    def p_enum(self, p):
        ''' enum : ENUM IDENTIFER LSWBR assignment_list RSWBR'''
        print("enum" , p)

    def p_definition_list_1(self, p):
        ''' definition_list : definition
                            | definition_list definition '''
        print("definition list" , p)

    def p_definition(self, p):
        ''' definition : DTYPE IDENTIFIER EQ NUMBER SEMICOLON '''

    def p_assignment_list(self, p):
        ''' assignment_list : assignment
                            | assignment_list assignment '''
        print("assignment_list" , p)

    def p_assignment(self, p):
        ''' assignment : IDENTIFIER EQ NUMBER SEMICOLON '''
        print("assignment" , p)



    def p_empty(self, t):
        'empty : '
        pass

    def p_error(self, t):
        print("Whoa. We're hosed")



if __name__ == '__main__':
    protoFile = 'test/data/alltypes_proto3/alltypes.proto'
    data=''
    with open(protoFile) as fd:
        data=fd.read()
    #pb_lex = PBLexer()
    #pb_lex.parse(data)
    pb_parse= PBParse()
    pb_parse.parse(data)

