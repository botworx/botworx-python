from contextlib import contextmanager
import trio
from asyncio import Future

class Message:
    def __init__(self, txt):
        self.txt = txt
        self.future = None


class Behavior:
    def __init__(self):
        self.bot = None
        self.children = []
        self.nursery = None

    def add(self, child):
        child.parent = self
        child.bot = self.bot
        self.children.append(child)

    async def main(self):
        print("I'm a Behavior")
        msg = Message('Bob')
        result = await self.bot.call(msg)
        print(result)
        print("I'm done")


class Bot(Behavior):
    def __init__(self):
        super().__init__()
        self.bot = self
        self.posts = []

    def run(self, debug=None):
        trio.run(self.main)

    async def main(self):
        print("I'm a Bot!")
        async with trio.open_nursery() as nursery:
            self.nursery = nursery
            for child in self.children:
                nursery.start_soon(child.main)

    async def process_posts(self):
        for post in self.posts:
            print("process")
            future = post.future
            future.set_result("Bob")
        print("later")

    async def call(self, msg):
        future = Future()
        msg.future = future
        self.posts.append(msg)
        posts = await self.process_posts()
        result = await future
        return result


@contextmanager
def action(parent):
    b = Behavior()
    if parent:
        parent.add(b)
    yield b


@contextmanager
def bot(parent=None):
    b = Bot()
    if parent:
        parent.add(b)
    yield b


with bot() as top:
    with action(top) as t:

        async def f(self):
            print("hi")

        # t.main = f


top.run()
