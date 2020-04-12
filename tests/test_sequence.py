from botworx.run.behavior import *

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