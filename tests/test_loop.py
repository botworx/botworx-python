from botworx.run.behavior import *

with timer(5) as top:
    with loop() as loop:
        with counter(1, 11) as cntr:
            with condition() as c:
                async def fn(b):
                    if cntr.count > 4:
                        await b.fail()
                    print('good')
                c.use(fn)
            with action() as a:
                async def fn(b):
                    print('a count: ', cntr.count)
                a.use(fn)

top.run(debug=True)
