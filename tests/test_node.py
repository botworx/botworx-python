import botworx.compile.ast.node as yy

obj = yy.Term('Bob')
print(vars(obj), obj.__class__)

obj = yy.term_('Joe')
print(vars(obj), obj.__class__)

obj = yy.Type('Eggs')
print(vars(obj), obj.__class__)

obj = yy.type_('Bacon')
print(vars(obj), obj.__class__)

obj = yy.Term('Henry')
print(vars(obj), obj.__class__)

obj = yy.term_('Frank')
print(vars(obj), obj.__class__)
