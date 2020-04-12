from botworx.run.behavior import *

with loop() as top:
    with counter(1, 11, top) as p:
        with condition(p) as c:
            async def fn(b):
                if p.count > 4:
                    await b.fail()
                print('good')

            c.use(fn)
        with action(p) as a:
            async def fn(b):
                print('a count: ', p.count)
            a.use(fn)

top.run(debug=True)
