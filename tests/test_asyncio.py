from contextlib import asynccontextmanager
import asyncio

#from botworx.run.task import Task
class Message:
    def __init__(self):
        self.future = None

class Task(asyncio.Task):
    def __init__(self, parent=None):
        super().__init__(self.main())
        self.parent = parent
        if parent:
            self.runner = parent.runner
            #parent.add(self)
        
    async def main(self):
        print("I'm a Task")
        msg = Message()
        #result  = await runner.call(msg)
        print(result)
        print("I'm done")

class Runner(Task):
    def __init__(self):
        super().__init__()
        self.runner = self
        self.posts = []
        #self.group = curio.TaskGroup()

    async def add(self, task):
        pass
        #await self.group.add_task(task)
        #print(self.group.tasks)
    '''
    async def run(self):
        #asyncio.run(coro, *, debug=False)
        #asyncio.run(self.main, debug=True)
        #asyncio.run(task, debug=True)
        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(task)
        #loop.run_forever()
        await self.main()
    '''
    async def main(self):
        print("I'm a Runner")
        await self.group.join()


    async def process_posts(self):
        for post in self.posts:
            print('process')
            future = post.future
            future.set_result(None)
        print('later')

    async def call(self, msg):
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        msg.future = future
        self.posts.append(msg)
        loop.create_task(self.process_posts())
        await future
        return 2


@asynccontextmanager
async def task(parent):
    t = Task(parent)
    yield t
    await parent.add(t)

@asynccontextmanager
async def runner():
    r = Runner()
    yield r
    #await r.main()

#loop = asyncio.get_event_loop()
#loop.run_until_complete(task)
async def main():
    async with runner() as r:
        async with task(r) as t:
            async def f(self):
                print('hi')
            t.main = f

loop = asyncio.get_event_loop()
loop.run_until_complete(main())