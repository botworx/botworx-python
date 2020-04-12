import curio
import asyncio

from botworx.run import *
from botworx.run import _I
from botworx.run.policy import Policy

class Agent(Policy):
    def __init__(self):
        super().__init__()
        self.posts = []

    def run(self):
        curio.run(self.main())

    async def main(self):
        print("I'm an Agent")

    async def process_posts(self):
        print('process')
        for post in self.posts:
            for rule in self.__class__.rules:
                print(rule)
                task = await curio.spawn(rule.action(self))
                await task.join()

    async def post(self, msg):
        self.posts.append(msg)
        await self.process_posts()

    async def call(self, msg):
        loop = self.loop
        future = loop.create_future()
        msg.future = future
        self.posts.append(msg)
        await self.process_posts()
        await future

_like = term_('like')
_Cheese = term_('Cheese')

class MyAgent(Agent):
    def __init__(self):
        super().__init__()
        print(self.__class__.rules)

    async def main(self):
        await self.post(assert_(Believe, _I, _like, _Cheese))

    @_(onAssert_(_I, _like, _Cheese))
    async def howdy(self):
        print('Howdy Folks!')

agent = MyAgent()
agent.run()
