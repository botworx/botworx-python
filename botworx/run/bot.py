from contextlib import asynccontextmanager
import curio
from asyncio import Future

from botworx.g import logger
from botworx.run import *
from botworx.run.behavior import Behavior

class Bot(Behavior):
    def __init__(self):
        super().__init__()
        self.bot = self
        self.posts = []

    async def main(self):
        print("I'm a Bot")
        for child in self.children:
            await self.tasks.spawn(child.main())
        await self.tasks.join()
    '''
    async def process_posts(self):
        for post in self.posts:
            print('process')
            future = post.future
            future.set_result('Bob')
        print('later')

    '''
    async def process_posts(self):
        print('process')
        for post in self.posts:
            await self.dispatch(post)

    async def dispatch(self, msg):
        T = type(msg)
        if T is Propose:
            logger.debug(f"* \t{msg}")
            pmsg = Attempt()
            pmsg.update(msg)

            self.proposals.append(pmsg)
            return
        elif T is Assert:
            logger.debug(f"+ \t{msg}")
            self.ctx.add(msg.data)
            return self.fire(msg)
        elif T is Retract:
            logger.debug(f"- \t${msg}")
            self.ctx.remove(msg.data)
            return self.fire(msg)
        else:
            logger.debug(f"Eval:\t{msg}")
            return await self.fire(msg)

    async def fire(self, msg):
        for m in self.policy.match(msg):
            print('fire', m)
            logger.debug(f"Fire:\t{m}:")
            task = await curio.spawn(m.rule.action(self, m))
            await task.join()

    async def post(self, msg):
        self.posts.append(msg)
        await curio.spawn(self.process_posts())

    async def call(self, msg):
        future = Future()
        msg.future = future
        self.posts.append(msg)
        posts = await curio.spawn(self.process_posts())
        await posts.join()
        result = await future
        return result
