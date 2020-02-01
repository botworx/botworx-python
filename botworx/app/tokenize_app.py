'''
'''
#import sys
#import os
from botworx.data import load
from botworx.compile.lex.lexer import Lexer
#
class App(object):
    
    def __init__(self):
        pass
        
    def run(self):
        f = load('blox.mia')
        lexer = Lexer()
        lexer.build()
        lexer.input_file(f)
        #print "Oops!  Nothing here to see!"
        while True:
            tok = lexer.token()
            if not tok: break      # No more input
            print(tok)
            