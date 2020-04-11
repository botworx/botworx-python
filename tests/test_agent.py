import asyncio
import types

from botworx.application import create_app
app = create_app()

from botworx.run import *
from botworx.run import _I
from botworx.run.agent import Agent

_jump = term_('jump')
_say = term_('say')
_x_ = var_('x')

class MyAgent(Agent):
    def __init__(self):
        super().__init__()
        print(self.__class__.rules)

    async def main(self):
        await self.post(attempt_(Achieve, _I, _jump))

    @_(OnAttempt(Achieve, _I, _jump))
    async def howhigh(self, msg):
        print('How high?')
        print(msg)

    @_(OnAttempt(Achieve, _I, _say, _x_))
    async def howdy(self, msg):
        print('Howdy Folks!')
        print(msg)

    @_(OnAttempt(Achieve, _I, _say, _x_))
    async def howfar(self, msg):
        print('How Far?')
        print(msg)

agent = MyAgent()

agent.run()