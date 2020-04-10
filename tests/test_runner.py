import asyncio
import types

from botworx.application import create_app
app = create_app()

from botworx.run import *
from botworx.run.runner import Runner


class MyRunner(Runner):
    def __init__(self):
        super().__init__()
        print(self.__class__.rules)
        self.post(Message('howdy'))

    @_('howdy')
    async def howdy(self):
        print('Howdy Folks!')

runner = MyRunner()
result = runner.run()
print(result)
#loop = asyncio.get_event_loop()
#loop.run_until_complete(task)