import contextvars
from contextlib import contextmanager
from uuid import uuid1
from copy import copy
import inspect
import trio

# from botworx.run.taskmeta import BehaviorMeta
# from botworx.run.policy import Policy
from botworx.run import *
from botworx.run.policy import Policy

TS_INITIAL = "Initial"
TS_RUNNING = "Running"
TS_SUCCESS = "Success"
TS_FAILURE = "Failure"
TS_SUSPENDED = "Suspended"
TS_HALTED = "Halted"

#
# Context Management
#
PARENT = "parent"

ctx_parent = contextvars.ContextVar("ctx_parent", default=None)


def ctx_enter(parent, child):
    if not parent:
        parent = ctx_parent.get()
    if parent:
        child.parent = parent
        parent.add(child)

    ctx_parent.set(child)
    return {PARENT: parent}


def ctx_exit(ctx):
    ctx_parent.set(ctx[PARENT])


# class Behavior(metaclass=BehaviorMeta):
class Behavior(Policy):
    def __init__(self):
        self.id = uuid1()
        self.rnr = None
        self.msg = None
        self.parent = None
        self.children = []
        self.result = None
        self.status = TS_INITIAL
        self.policy = self
        self.tasks = None

    def add(self, child):
        child.parent = self
        child.tasks = self.tasks
        self.children.append(child)
        return self

    def remove(self, child):
        index = self.children.indexOf(child)
        if index > -1:
            self.children.splice(index, 1)
        return self

    def use(self, fn):
        self.main = fn

    def define(self, trigger, action):
        return self.addRule(Rule(trigger, action))

    def sig(self, trigger, action):
        # self.rnr.signal(trigger, self)
        return self.define(trigger, action)

    def addRule(self, r):
        if not self.policy:
            self.policy = Policy(self)
        return self.policy.add(r)

    def findRule(self, m):
        return self.findRules(m).pop()

    def findRules(self, m):
        if self.policy:
            return self.policy.find(m)
        return []

    def matchRule(self, m):
        return self.matchRules(m).pop()

    def matchRules(self, m):
        if self.policy:
            return self.policy.match(m)
        return []

    #
    # EXECUTION
    #
    async def strategy(self, child):
        status = child.status
        if status == TS_FAILURE:
            raise Failure()
            return status
        elif status == TS_SUCCESS:
            return status

    def run(self, debug=None):
        trio.run(self.main)

    def suspend(self):
        self.status = TS_SUSPENDED
        return self.status

    def resume(self):
        self.status = TS_RUNNING
        return self.status

    def succeed(self):
        self.status = TS_SUCCESS
        return self.status

    async def fail(self):
        print("fail")
        self.status = TS_FAILURE
        if self.parent:
            return await self.parent.strategy(self)
        else:
            return self.status

    def halt(self):
        if self.rnr:
            self.rnr.halt()
        self.status = TS_HALTED
        return self.status

    def broadcast(self, msg):
        pass

    def post(self, msg):
        msg.sender = self
        return self.rnr.post(msg)

    def spawn(self, o, wait=False):
        task = None
        if type(o, function):
            task = Behavior(o)
        elif isinstance(o, Behavior):
            task = o
        else:
            raise Error("Expecting Function or Behavior")
        if wait:
            task.caller = self

        return self.rnr.schedule(task)

    def call(self, s, p, o, x):
        c = Achieve(s, p, o, x)
        m = Attempt(c, self)
        m.caller = self
        self.post(m)
        return self.suspend()

    def perform(self, s, p, o, x):
        c = Achieve(s, p, o, x)
        m = Attempt(c, self)
        return self.post(m)

    def propose(self, c):
        return self.post(Propose(c, self))

    def attempt(self, c):
        return self.post(Attempt(c, self))

    def declare(self, c):
        return self.post(Assert(c, self))

    def retract(self, c):
        return self.post(Retract(c, self))

    #
    # Utility
    #
    def toJSON(self):
        return {TYPE: self.__class__.__name, MSG: self.msg}

    #
    # DSL
    #
    def chain(self, b):
        a = self.children[self.children.length - 1]
        if a:
            a.dst = b
            b.src = a
        self.add(b)
        return self


#
# Condition
#
class Condition(Behavior):
    pass


@contextmanager
def condition(parent=None):
    child = Condition()
    ctx = ctx_enter(parent, child)
    yield child
    ctx_exit(ctx)


condition_ = lambda: Condition()

#
# Action
#
class Action(Behavior):
    pass


@contextmanager
def action(parent=None):
    child = Action()
    ctx = ctx_enter(parent, child)
    yield child
    ctx_exit(ctx)


action_ = lambda action: Action(action)


#
# Sequence
#
class Sequence(Behavior):
    def __init__(self):
        super().__init__()

    async def main(self):
        for child in self.children:
            result = await child.main()
            if result == TS_FAILURE:
                return await self.fail()


@contextmanager
def sequence(parent=None):
    child = Sequence()
    ctx = ctx_enter(parent, child)
    yield child
    ctx_exit(ctx)


#
# Loop
#
class Timer(Behavior):
    def __init__(self, timeout):
        super().__init__()
        self.timeout = timeout

    async def main(self):
        with trio.move_on_after(self.timeout):
            while True:
                for child in self.children:
                    try:
                        async with trio.open_nursery() as tasks:
                            tasks.start_soon(child.main)
                    except Failure:
                        return


@contextmanager
def timer(timeout, parent=None):
    child = Timer(timeout)
    ctx = ctx_enter(parent, child)
    yield child
    ctx_exit(ctx)


#
# Loop
#
class Loop(Behavior):
    def __init__(self):
        super().__init__()

    async def main(self):
        while True:
            for child in self.children:
                try:
                    async with trio.open_nursery() as tasks:
                        tasks.start_soon(child.main)
                except Failure:
                    return


@contextmanager
def loop(parent=None):
    child = Loop()
    ctx = ctx_enter(parent, child)
    yield child
    ctx_exit(ctx)


#
# Counter
#
class Counter(Behavior):
    def __init__(self, start, stop):
        super().__init__()
        self.start = start
        self.stop = stop
        self.count = 0

    async def main(self):
        for i in range(self.start, self.stop):
            self.count = i
            for child in self.children:
                try:
                    async with trio.open_nursery() as tasks:
                        tasks.start_soon(child.main, child)
                except Failure:
                    return


@contextmanager
def counter(start, stop, parent=None):
    child = Counter(start, stop)
    ctx = ctx_enter(parent, child)
    yield child
    ctx_exit(ctx)


#
# Parallel
#
class Parallel(Behavior):
    def __init__(self):
        super().__init__()

    async def main(self):
        async with trio.open_nursery() as tasks:
            self.tasks = tasks
            for child in self.children:
                tasks.start_soon(child.main)
        return self.suspend()


@contextmanager
def parallel(parent=None):
    child = Parallel()
    ctx = ctx_enter(parent, child)
    yield child
    ctx_exit(ctx)


#
# Chain
#
class Chain(Behavior):
    def __init__(self, action):
        super().__init__(action)

    def main(self):
        child = self.children[0]
        self.rnr.schedule(child)
        return self.suspend()

    def strategy(self, child):
        self.remove(child)
        if child.status == TS_FAILURE:
            return self.fail()
        if child.dst:
            return self.rnr.schedule(child.dst)


chain_ = lambda action: Chain(action)


#
# Method
#
class Method(Sequence):
    pass


method_ = lambda action: Method(action)

#
# Module
#
class Module(Method):
    pass


module_ = lambda action: Module(action)

sequence_ = lambda action: Sequence(action)

counter_ = lambda start, stop, action: Counter(start, stop, action)

parallel_ = lambda action: Parallel(action)
