class Agency:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    async def send(self, msg):
        asyncio.create_task(self.publish(msg))

    async def publish(self, msg):
        for subscriber in self.subscribers:
            await subscriber.send(msg)
