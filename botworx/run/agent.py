import asyncio
import types

from botworx.g import logger
from botworx.run import *
from botworx.run.policy import Policy

class Message:
    def __init__(self, txt):
        self.future = None
        self.txt = txt

class Agent(Policy):
    def __init__(self):
        super().__init__()
        self.loop = asyncio.get_event_loop()
        self.posts = []
        self.policy = self

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
            self.dispatch(post)
            '''
            for rule in self.__class__.rules:
                print(rule)
                if(rule[0] == post.txt):
                    self.loop.create_task(rule[1](self))
            '''
            '''
            future = post.future
            if future:
                future.set_result(None)
            '''
    def dispatch(self, msg):
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
            return self.fire(msg)

    def fire(self, msg):
        print('fire', msg)
        for m in self.policy.match(msg):
            print('fire', m)
            logger.debug(f"Fire:\t{m}:")
            self.loop.create_task(m.rule.action(self))

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
