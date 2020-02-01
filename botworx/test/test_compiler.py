'''
'''
#import sys
#import os
import unittest
import pprint
import json

from botworx.data import load
from botworx.compile.lex.lexer import Lexer
from botworx.compile.parse.parser import Parser
from botworx.compile.ast.node import AstEncoder
from botworx.compile.compiler import Compiler
#
class Test(unittest.TestCase):
    
    def test(self):
        #f = load('blox.mia')
        f = load('hello.mia')
        s = f.read()
        print('##start##')
        print(s)
        print('##end##')
        
        lexer = Lexer()
        lexer.build()
        #
        parser = Parser(lexer)
        parser.build()
        #ast = parser.parse(s, debug=1)
        ast = parser.parse(s)
        #print ast
        #pprint.pprint(ast)
        #json.dumps(ast)
        print( AstEncoder(indent=2).encode(ast) )
        #
        compiler = Compiler()
        compiler.compile(ast)
        
        
        