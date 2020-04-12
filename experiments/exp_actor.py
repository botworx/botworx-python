import unittest

from botworx.run.actor import Actor

class TestActor(Actor):

    @_('+ $x likes Turtles')
    def blah():
        print('blah')

    @_('+ $x likes Turtle Soup')
    def blah():
        print('blah')

actor = TestActor()

print(vars(policy.__class__))

class Test(unittest.TestCase):
    def test(self):
        pass

if __name__ == '__main__':
    unittest.main()