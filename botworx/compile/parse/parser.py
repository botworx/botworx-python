
import ply.yacc as yacc
from botworx.compile.lex.tokens import tokens
from botworx.compile.ast.node import *

class Parser(object):
    tokens = tokens
    def __init__(self, lexer):
        self.lexer = lexer
    
    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        
    def parse(self, s, **kwargs):
        return self.parser.parse(s, lexer=self.lexer, **kwargs)
    #   
    def p_root_empty(self, p):
        'Root : '
        p[0] = Block()
        
    def p_root_body(self, p):
        'Root : Body'
        p[0] = p[1]
        
    def p_root_block(self, p):
        'Root : Block TERMINATOR'
        p[0] = p[1]
        
    def p_block_body(self, p):
        'Block : INDENT Body DEDENT'
        p[0] = p[2]
        
    def p_body_line(self, p):
        'Body : Line'
        p[0] = Block([p[1]])
        
    def p_body_body_line(self, p):
        'Body : Body TERMINATOR Line'
        p[1].push(p[3])
        p[0] = p[1]
        
    def p_body_body(self, p):
        'Body : Body TERMINATOR'
        p[0] = p[1]
        
    def p_line(self, p):
        '''Line : Expression
                | Statement'''
        p[0] = p[1]
       
    def p_expr(self, p):
        '''Expression : Clause
                | Term'''
        p[0] = p[1]
        
    def p_term(self, p):
        '''Term : VARIABLE
                | NOUN
                | STRING'''
        p[0] = p[1]
        
    def p_snippet(self, p):
        'Term : SNIPPET'
        p[0] = Snippet(p[1])
        
    def p_parexpr(self, p):
        'ParExpr : LPAR Expression RPAR'
        p[0] = p[2]
        
    def p_parexpr_empty(self, p):
        'ParExpr : LPAR RPAR'
        p[0] = None
        
    def p_stmt(self, p):
        '''Statement : Class
                     | Method'''
        p[0] = p[1]
        
    def p_class(self, p):
        'Class : CLASS Identifier Block'
        p[0] = Class(p[2], p[3])
        
    def p_def(self, p):
        'Method : DEF Identifier ParExpr Block'
        p[0] = Method(p[2], p[3], p[4])
        
    def p_clause1(self, p):
        ' Clause : Expression VERB Expression'
        p[0] = Clause(p[1], p[2], p[3]);
        
    def p_clause2(self, p):
        'Clause : Expression VERB'
        p[0] = Clause(p[1], p[2], None);

    def p_clause3(self, p):
        'Clause : VERB Expression'
        p[0] = Clause(None, p[1], p[2]);

    def p_clause4(self, p):
        'Clause : VERB'
        p[0] = Clause(None, p[1], None);
        
    def p_clause5(self, p):
        'Clause : Expression'
        p[0] = p[1]
        
    def p_id(self, p):
        '''Identifier : VERB
                    | NOUN'''
        p[0] = p[1]
    '''                
    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")
    '''