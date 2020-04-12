import unittest

from botworx.run.behavior import *


class Test(unittest.TestCase):
    def test(self):
        with counter(1, 11) as p:
            with action(p) as a:
                async def fn(obj):
                    print('count: ',obj.parent.count)
                a.use(fn)
        p.run()

if __name__ == '__main__':
    unittest.main()