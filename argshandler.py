from core.argshandler import Handler

class CustomHandler(Handler):
    def __init__(self, args):
        super().__init__(args)
    
    def all(self):
        return self.args.all
    
    def db(self):
        return self.args.db
    
    def toggle(self):
        return self.args.toggle

    def new(self):
        return self.args.new
    
    def update(self):
        return self.args.update
    
    def status(self):
        return self.args.status
