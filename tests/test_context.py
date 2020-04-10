from botworx.run import *
from botworx.run.context import Context

_Bob = term_('Bob')
_likes = term_('likes')
_Toast = term_('Toast')

ctx = Context()
ctx.add(believe_(_Bob, _likes, _Toast))
print(ctx)