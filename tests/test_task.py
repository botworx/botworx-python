import asyncio
import types

#from botworx.run.task import Task
class Message:
    def __init__(self):
        self.future = None

class Task(asyncio.tasks.Task):
    def __init__(self, runner=None):
        super().__init__(self.main())
        self.runner = runner
        
    async def main(self):
        print("I'm a Task")
        msg = Message()
        result  = await runner.call(msg)
        print(result)
        print("I'm done")

class Runner(Task):
    def __init__(self, runner=None):
        super().__init__()
        self.posts = []

    def run(self, task):
        #asyncio.run(coro, *, debug=False)
        #asyncio.run(self.main, debug=True)
        #asyncio.run(task, debug=True)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(task)
        #loop.run_forever()

    async def main(self):
        print("I'm a Runner")


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


runner = Runner()
task = Task(runner)

result = runner.run(task)
print(result)
#loop = asyncio.get_event_loop()
#loop.run_until_complete(task)