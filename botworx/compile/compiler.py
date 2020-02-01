from botworx.compile.ast.visitor import Visitor
from botworx.compile.ast.policy import Policy
    
def beginNodeVisit(t, n):
    t.write(''.join(['//begin ', n.kind]))

def beginSnippetVisit(t, n):
    t.write(n.code)

def endNodeVisit(t, n):
    t.write(''.join(['//end ', n.kind]))
#
def beginBlockVisit(t, n):
    beginNodeVisit(t, n)
    for c in n.children:
        t.visit(c)

def endBlockVisit(t, n):
  endNodeVisit(t, n) 
#
def beginClassDefVisit(t, n):
    t.save()
    t.classDef = n
    t.write(''.join(['var ', n.name, ' = (function() {']))
    t.indent()
    t.visit(n.block)
    t.dedent()
    t.restore()

def endClassDefVisit(t, n):
    t.write('})();')
    endBlockVisit(t, n)
#
def beginMethodDefVisit(t, n):
    name = n.name
    className = t.classDef.name
    if(name == 'constructor'):
        name = className
        t.write(''.join(['function ', name, '() {']))
    else:
        t.write(''.join([className, '.prototype.', name, ' = function() {']));
    t.indent()
    t.visit(n.block)
  
def endMethodDefVisit(t, n):
    t.dedent()
    t.write('}')
#
policies = {
    'Block': Policy(
        beginBlockVisit,
        endBlockVisit
    ),
    'Class': Policy(
        beginClassDefVisit,
        endClassDefVisit
    ),  
    'Predicate': Policy(
        beginNodeVisit,
        endNodeVisit
    ),
    'Method': Policy(
        beginMethodDefVisit,
        endMethodDefVisit
    ),
    'BinaryExpr': Policy(
        beginNodeVisit,
        endNodeVisit
    ),
    'UnaryExpr': Policy(
        beginNodeVisit,
        endNodeVisit
    ),  
    'Clause': Policy(
        beginNodeVisit,
        endNodeVisit
    ),
    'Where': Policy(
        beginNodeVisit,
        endNodeVisit
    ),
    'Snippet': Policy(
        beginSnippetVisit,
        endNodeVisit
    )    
}

class State(object):
    def __init__(self, classDef):
        self.classDef = classDef
    
class Compiler(Visitor):
    def __init__(self):
        self.policies = policies;
        self.out = [];
        self.indentlevel = 0;
        self.indentation = '';
        self.states = [];
        #
        self.classDef = None;
        
    def compile(self, ast):
        self.visit(ast)

    def save(self):
        state = State(self.classDef)
        self.states.append(state);

    def restore(self):
        state = self.states.pop();
        self.classDef = state.classDef;

    def write(self, s):
        print(self.indentation + s)
        
    def indent(self):
        self.indentlevel += 1 ;
        self.indentation = '  ' * (self.indentlevel + 1)
        
    def dedent(self):
        self.indentlevel -= 1 ;
        self.indentation = '  ' * (self.indentlevel + 1)
        

        