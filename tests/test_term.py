from botworx.run import *

bob = term_('Bob')
print(bob, bob.__class__.__name__)
bob2 = term_('Bob')

print(bob == bob2)

jump = term_('jump')
print(jump, jump.__class__.__name__)