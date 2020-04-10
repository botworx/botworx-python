import asyncio
import types

from botworx.run.policy import Policy

class Message:
    def __init__(self, txt):
        self.future = None
        self.txt = txt

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

class Agent(Policy):
    def __init__(self):
        super().__init__()
        self.loop = asyncio.get_event_loop()
        self.posts = []

    def run(self):
        #asyncio.run(coro, *, debug=False)
        #asyncio.run(self.main, debug=True)
        #asyncio.run(task, debug=True)
        self.loop.run_until_complete(self.main())
        #loop.run_forever()

    async def main(self):
        print("I'm an Agent")


    async def process_posts(self):
        print('process')
        for post in self.posts:
            for rule in self.__class__.rules:
                print(rule)
                if(rule[0] == post.txt):
                    self.loop.create_task(rule[1](self))

            '''
            future = post.future
            if future:
                future.set_result(None)
            '''
    def post(self, msg):
        self.posts.append(msg)
        self.loop.create_task(self.process_posts())

    async def call(self, msg):
        loop = self.loop
        future = loop.create_future()
        msg.future = future
        self.posts.append(msg)
        loop.create_task(self.process_posts())
        await future
        return 2


class MyAgent(Agent):
    def __init__(self):
        super().__init__()
        print(self.__class__.rules)
        self.post(Message('howdy'))

    @_('howdy')
    async def howdy(self):
        print('Howdy Folks!')

agent = MyAgent()
result = agent.run()
print(result)
#loop = asyncio.get_event_loop()
#loop.run_until_complete(task)