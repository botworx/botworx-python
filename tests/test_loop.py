import unittest

from botworx.run.behavior import *


class Test(unittest.TestCase):
    def test(self):
        with timer(0.5) as top:
            with loop() as l:
                with counter(1, 11) as cntr:
                    with condition() as c:

                        async def fn(b):
                            if cntr.count > 5:
                                await b.fail()
                            print("good")

                        c.use(fn)
                    with action() as a:

                        async def fn(b):
                            print("a count: ", cntr.count)

                        a.use(fn)

        top.run(debug=True)


if __name__ == "__main__":
    unittest.main()
