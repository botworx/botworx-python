import unittest

from botworx.run.behavior import *

class Test(unittest.TestCase):
    def test(self):
        with sequence() as s:
            with action() as a:
                async def fn():
                    print('Hi')
                a.main = fn
            with action() as a:
                async def fn():
                    print('Bye')
                a.main = fn

        s.run()

if __name__ == '__main__':
    unittest.main()