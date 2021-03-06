import unittest

from botworx.data import load
from botworx.compile.lex.lexer import Lexer

class Test(unittest.TestCase):
    def test(self):
        filename = "turtles.mia"

        with load(filename) as fh:
            s = fh.read()
            
        lexer = Lexer()
        tokens = lexer.tokenize(s)
        for tok in tokens:
            print(tok)


if __name__ == "__main__":
    Test().test()
