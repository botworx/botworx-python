#! /usr/bin/env python

#import sys
#import os

'''
try:
    __file__
except NameError:
    pass
else:
    libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib'))
    sys.path.insert(0, libdir)
'''
from botworx.app.tokenize_app import App

app = App()
app.run()