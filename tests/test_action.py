from botworx.run.behavior import *

with action() as a:
    async def fn():
        print('Hi')
    a.main = fn
    a.run()