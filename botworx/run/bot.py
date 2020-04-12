from contextlib import asynccontextmanager
import trio
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
        async with trio.open_nursery() as tasks:
            self.tasks = tasks
            for child in self.children:
                tasks.start_soon(child.main())

    async def process_posts(self):
        print("process")
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
            print("fire", m)
            logger.debug(f"Fire:\t{m}:")
            await m.rule.action(self, m)

    async def post(self, msg):
        self.posts.append(msg)
        await self.process_posts()

    async def call(self, msg):
        future = Future()
        msg.future = future
        self.posts.append(msg)
        await self.process_posts()
        result = await future
        return result
