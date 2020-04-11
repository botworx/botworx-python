import inspect
from contextlib import *

class Test(AbstractContextManager):
    def __init__(self):
        self.coro = None
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        print(type)
        pass

def main():
    with Test() as t:
        def fn():
            print('fn')
        t.coro = fn
        v = inspect.getmembers(t)
        print(v)

main()