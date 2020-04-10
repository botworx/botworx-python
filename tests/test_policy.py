import unittest

from botworx.run.policy import Policy

class TestPolicy(Policy):

    @_('+ $x likes Turtles')
    def blah():
        print('blah')

    @_('+ $x likes Turtle Soup')
    def blah():
        print('blah')

policy = TestPolicy()

print(vars(policy.__class__))

class Test(unittest.TestCase):
    def test(self):
        pass

if __name__ == '__main__':
    unittest.main()