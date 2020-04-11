from botworx.run.behavior import *

with sequence() as s:
    with action(s) as a:
        async def fn():
            print('Hi')
        a.main = fn
    with action(s) as a:
        async def fn():
            print('Bye')
        a.main = fn

s.run()