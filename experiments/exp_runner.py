import asyncio


class Message:
    def __init__(self, id, kind='default', ok=True):
        self.id = id
        self.kind = kind
        self.ok = ok

class Subscriber:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.active = True

    def send(self, msg):
        pass

    async def receive(self):
        await self.queue.get()

class Hub:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    async def send(self, msg):
        asyncio.create_task(self.publish(msg))

    async def publish(self, msg):
        for subscriber in self.subscribers:
            await subscriber.send(msg)

hub = Hub()

class PostSubscriber(Subscriber):
    def __init__(self, id):
        super().__init__()
        self.id = id

    async def send(self, msg):
        print('put in queue')
        if msg.id != self.id:
            return
        await self.queue.put(msg)

class Runner:
    def run(self, task):
        #asyncio.run(coro, *, debug=False)
        #asyncio.run(self.main, debug=True)
        asyncio.run(task, debug=True)
        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(task)
        #loop.run_forever(task)

    async def main(self):
        print('hello')


task = Task()
runner = Runner()
runner.run(task)
#loop = asyncio.get_event_loop()
#loop.run_until_complete(task)