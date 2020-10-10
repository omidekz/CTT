import abc
from argparse import ArgumentParser

class Handler(metaclass=abc.ABCMeta):
    def __init__(self, args):
        self.args = args
    
    @abc.abstractclassmethod
    def all(self) -> bool:
        pass
    
    @abc.abstractclassmethod
    def db(self) -> str:
        pass
    
    @abc.abstractclassmethod
    def toggle(self) -> str:
        return self.args.toggle
    
    @abc.abstractclassmethod
    def new(self) -> [[str, dict]]:
        return self.new
    
    @abc.abstractclassmethod
    def update(self) -> dict:
        pass
    
    @abc.abstractclassmethod
    def status(self):
        pass
