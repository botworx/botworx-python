from contextlib import asynccontextmanager
import curio
from asyncio import Future
#from botworx.run.task import Task
class Message:
    def __init__(self):
        self.future = None

class Task():
    def __init__(self, parent=None):
        self.parent = parent
        if parent:
            self.runner = parent.runner
            #parent.add(self)
        
    async def main(self):
        print("I'm a Task")
        msg = Message()
        result  = await self.runner.call(msg)
        print(result)
        print("I'm done")

class Runner:
    def __init__(self):
        super().__init__()
        self.runner = self
        self.posts = []
        self.group = curio.TaskGroup()

    async def add(self, task):
        await self.group.spawn(task.main())
        print(self.group.tasks)

    async def main(self):
        print("I'm a Runner")
        await self.group.join()

    async def process_posts(self):
        for post in self.posts:
            print('process')
            future = post.future
            future.set_result('Bob')
        print('later')

    async def call(self, msg):
        future = Future()
        msg.future = future
        self.posts.append(msg)
        posts = await curio.spawn(self.process_posts())
        await posts.join()
        result = await future
        return result


@asynccontextmanager
async def task(parent):
    t = Task(parent)
    yield t
    await parent.add(t)

@asynccontextmanager
async def runner():
    r = Runner()
    yield r
    await r.main()

async def main():
    async with runner() as r:
        async with task(r) as t:
            async def f(self):
                print('hi')
            #t.main = f

curio.run(main())