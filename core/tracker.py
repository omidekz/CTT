from . import BaseManager
from . import Handler

class Core:
    def __init__(self, manager: BaseManager, args: Handler):
        self.manager = manager
        self.args = args
    
    def done(self):
        if self.args.all():
            pass
