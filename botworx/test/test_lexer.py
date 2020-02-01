'''
'''
#import sys
#import os
import unittest

from botworx.data import load
from botworx.compile.lex.lexer import Lexer

data = '''
class HelloWorld

  def constructor()
    say 'Hello World'
    
  def say(say $t)
    | print t
'''

class Test(unittest.TestCase):
    
    def test(self):
        f = load('hello.mia')
        lexer = Lexer()
        lexer.build()
        #lexer.input_file(f)
        lexer.input(data)
        print(lexer.lexer.lexdata)
        print(lexer.lexer.lexpos)
        while True:
            tok = lexer.token()
            if not tok:
                break      # No more input
            print(tok)

if __name__ == '__main__':
    Test().test()
