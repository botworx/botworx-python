import unittest

def match(v, p, b = {}):
    if isinstance(p, Var):
        b[p.name] = v
        return b
    if v == p:
        return b
    return False

class Term:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

def intern(name):
    return Term(name)

class Var:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

class Clause:
    def __init__(self, s, v, o, **xtra):
        self.subj = s
        self.verb = v
        self.obj = o
        for key, value in xtra.items():
            setattr(self, key, value)
    def __str__(self):
        return str(self.subj) + " " + str(self.verb) + " " + str(self.obj)


_Bob = intern("Bob")
_likes = intern("likes")
_Fish = intern("Fish")

class Test(unittest.TestCase):
    def test(self):
        c = Clause(_Bob, _likes, _Fish)
        print(c)
