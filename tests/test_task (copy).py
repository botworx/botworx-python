import asyncio
import types

#from botworx.run.task import Task

class Task(asyncio.tasks.Task):
    def __init__(self, runner=None):
        super().__init__(self.main())
        self.queue = asyncio.Queue()
        self.runner = runner
        
    async def main(self):
        print("I'm a Task")
        result  = await runner.call()
        print(result)
        print("I'm done")

class Runner(Task):
    def run(self, task):
        #asyncio.run(coro, *, debug=False)
        #asyncio.run(self.main, debug=True)
        #asyncio.run(task, debug=True)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(task)
        #loop.run_forever()

    async def main(self):
        print("I'm a Runner")

    @types.coroutine
    def suspend(self, fn):
        cont = yield
        fn(cont)
        cont_retval = yield
        return cont_retval

    def resume_later(self, fn):
        print('later')
        print(fn)

    async def call(self):
        self.suspend(self.resume_later)
        # return 2


runner = Runner()
task = Task(runner)

result = runner.run(task)
print(result)
#loop = asyncio.get_event_loop()
#loop.run_until_complete(task)