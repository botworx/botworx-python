import unittest

from botworx.run.behavior import *


class Test(unittest.TestCase):
    def test(self):
        with parallel() as top:
            with counter(1, 11) as p:
                with action() as a:
                    async def fn(obj):
                        print('a count: ', p.count)
                    a.use(fn)
            with counter(1, 6) as q:
                with action() as a:
                    async def fn(obj):
                        print('b count: ', q.count)
                    a.use(fn)

        top.run()

if __name__ == '__main__':
    unittest.main()