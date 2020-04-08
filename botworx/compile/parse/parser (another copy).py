
import sly

from botworx.compile.lex.lexer import Lexer
from botworx.compile.ast.node import *

class Parser(sly.Parser):
    tokens = Lexer.tokens
    def __init__(self):
        super().__init__()
            
    @_('Root : ')
    def p_root_empty(self, p):
        p[0] = Block()

    @_('Root : Body')
    def p_root_body(self, p):
        p[0] = p[1]

    @_('Root : Block TERMINATOR')
    def p_root_block(self, p):
        p[0] = p[1]

    @_('Block : INDENT Body DEDENT')
    def p_block_body(self, p):
        p[0] = p[2]

    @_('Body : Line')
    def p_body_line(self, p):
        p[0] = Block([p[1]])

    @_('Body : Body TERMINATOR Line')
    def p_body_body_line(self, p):
        p[1].push(p[3])
        p[0] = p[1]

    @_('Body : Body TERMINATOR')
    def p_body_body(self, p):
        p[0] = p[1]

    @_('Line : Expression', 'Line : Statement')
    def p_line(self, p):
        p[0] = p[1]
       
    @_('Expression : Clause', 'Expression : Term')
    def p_expr(self, p):
        p[0] = p[1]

    @_('Term : VARIABLE', 'Term : NOUN', 'Term : STRING')
    def p_term(self, p):
        p[0] = p[1]

    @_('Term : SNIPPET')
    def p_snippet(self, p):
        p[0] = Snippet(p[1])

    @_('ParExpr : LPAR Expression RPAR')
    def p_parexpr(self, p):
        p[0] = p[2]

    @_('ParExpr : LPAR RPAR')
    def p_parexpr_empty(self, p):
        p[0] = None

    @_('Statement : Class', 'Statement : Method')
    def p_stmt(self, p):
        p[0] = p[1]

    @_('Class : CLASS Identifier Block')
    def p_class(self, p):
        p[0] = Class(p[2], p[3])
    
    @_('Method : DEF Identifier ParExpr Block')
    def p_def(self, p):
        p[0] = Method(p[2], p[3], p[4])
        
    def p_clause1(self, p):
        ' Clause : Expression VERB Expression'
        p[0] = Clause(p[1], p[2], p[3]);
        
    @_('Clause : Expression VERB')
    def p_clause2(self, p):
        p[0] = Clause(p[1], p[2], None);

    @_('Clause : VERB Expression')
    def p_clause3(self, p):
        p[0] = Clause(None, p[1], p[2]);

    @_('Clause : VERB')
    def p_clause4(self, p):
        p[0] = Clause(None, p[1], None);
        
    @_('Clause : Expression')
    def p_clause5(self, p):
        p[0] = p[1]

    @_('Identifier : VERB', 'Identifier : NOUN')        
    def p_id(self, p):
        p[0] = p[1]
                    
    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")
