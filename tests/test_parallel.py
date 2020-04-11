from botworx.run.behavior import *

with parallel() as top:
    with counter(1, 11, top) as p:
        with action(p) as a:
            async def fn(obj):
                print('a count: ', p.count)
            a.use(fn)
    with counter(1, 6, top) as q:
        with action(q) as a:
            async def fn(obj):
                print('b count: ', q.count)
            a.use(fn)

top.run()
