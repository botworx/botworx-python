from botworx.run.behavior import *

with counter(1, 11) as p:
    with action(p) as a:
        async def fn(obj):
            print('count: ',obj.parent.count)
        a.use(fn)
p.run()