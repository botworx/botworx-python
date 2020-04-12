import unittest

from botworx.run.behavior import *

class Test(unittest.TestCase):
    def test(self):
        with action() as a:

            async def fn():
                print("Hi")

            a.use(fn)
            a.run()

if __name__ == '__main__':
    unittest.main()
