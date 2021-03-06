import asyncio

from botworx.run import *
from botworx.run import _I
from botworx.run.policy import Policy

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
                self.loop.create_task(rule.action(self))

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

_like = term_('like')
_Cheese = term_('Cheese')

class MyAgent(Agent):
    def __init__(self):
        super().__init__()
        print(self.__class__.rules)
        self.post(assert_(Believe, _I, _like, _Cheese))

    @_(onAssert_(_I, _like, _Cheese))
    async def howdy(self):
        print('Howdy Folks!')

agent = MyAgent()
agent.run()
