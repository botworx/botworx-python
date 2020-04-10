import botworx.g
from botworx.logging import create_logger

def create_app():
    botworx.g.logger = logger = create_logger()