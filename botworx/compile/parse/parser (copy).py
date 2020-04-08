
import sly

from botworx.compile.lex.lexer import Lexer
from botworx.compile.ast.node import *

class Parser(sly.Parser):
    tokens = Lexer.tokens
    def __init__(self):
        super().__init__()
            
    @_('')
    def root(self, p):
        return Block()

    @_('body')
    def root(self, p):
        return p[0]
        
    @_('block TERMINATOR')
    def root(self, p):
        return p[0]
        
    @_('INDENT body DEDENT')
    def block(self, p):
        return p[1]

    @_('line')
    def body(self, p):
        return Block([p[0]])

    @_('body TERMINATOR line')
    def body(self, p):
        p[0].push(p[2])
        return p[0]

    @_('body TERMINATOR')
    def body(self, p):
        return p[0]

    @_('expression', 'statement')
    def line(self, p):
        return p[0]
       
    @_('clause', 'term')
    def expression(self, p):
        return p[0]

    @_('VARIABLE', 'NOUN', 'STRING')
    def term(self, p):
        return p[0]

    @_('SNIPPET')
    def term(self, p):
        return Snippet(p[0])

    @_('LPAR expression RPAR')
    def par_expr(self, p):
        return p[1]

    @_('LPAR RPAR')
    def par_expr(self, p):
        return None
        
    @_('klass', 'method')
    def statement(self, p):
        return p[0]

    @_('CLASS identifier block')
    def klass(self, p):
        return Class(p[1], p[2])

    @_('DEF identifier par_expr block')
    def method(self, p):
        return Method(p[1], p[2], p[3])

    @_('expression VERB expression')
    def clause(self, p):
        return Clause(p[0], p[1], p[2]);

    @_('expression VERB')
    def clause(self, p):
        return Clause(p[0], p[1], None);

    @_('VERB expression')
    def clause(self, p):
        return Clause(None, p[0], p[1]);

    @_('VERB')
    def clause(self, p):
        return Clause(None, p[0], None);

    @_('expression')
    def clause(self, p):
        return p[0]

    @_('VERB', 'NOUN')
    def identifier(self, p):
        return p[0]
