import abc
from typing import List

class STATES:
	END = False
	PROGRESS = True

	@staticmethod
	def str(state):
		return 'end' if STATES.END == state else 'progress'
	
	@staticmethod
	def value(state):
		return STATES.END if state == STATES.END else STATES.PROGRESS
	
	@staticmethod
	def is_progress(state):
		return STATES.PROGRESS == state
	
	@staticmethod
	def is_end(state):
		return STATES.END == state

class BaseManager(metaclass=abc.ABCMeta):
	def __init__(self, db_path):
		self.db_path = db_path

	@abc.abstractmethod
	def write(self, lable, time=None) -> int:
		# return time of task in secs
		pass

	@abc.abstractmethod
	def read(self, lable) -> [int, str, str]:
		# return a list that i called resp
		# resp[0] => time on this lable in secs
		# resp[1] => lable
		# resp[2] => state of this lable that can be (STOP | PROGRESS)
		pass
	
	@abc.abstractmethod
	def exists(self, lable):
		pass
	
	@abc.abstractmethod
	def all(self):
		pass
