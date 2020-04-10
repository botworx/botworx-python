import asyncio
import types

from botworx.application import create_app
app = create_app()

from botworx.run import *
from botworx.run import _I
from botworx.run.agent import Agent

_say = term_('say')
_x_ = var_('x')

class MyAgent(Agent):
    def __init__(self):
        super().__init__()
        print(self.__class__.rules)
        self.post(attempt_(Achieve, _I, _say, 'jump!'))

    @_(OnAttempt(Achieve, _I, _say, _x_))
    async def howdy(self):
        print('Howdy Folks!')

agent = MyAgent()
result = agent.run()
print(result)
#loop = asyncio.get_event_loop()
#loop.run_until_complete(task)