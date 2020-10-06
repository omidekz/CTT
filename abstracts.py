import abc

class ReadResponse:
	def __init__(self, lable, whole_time, times, **kwargs):
		self.lable = lable
		self.whole_secs = whole_time
		self.times = times
		self.kwargs = kwargs
	
	def __str__(self):
		return str(
			{
				"lable": self.lable,
				"time_in_sec": self.whole_secs,
				"kwargs": self.kwargs
			}
		)

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
	def toggle(self, lable, time=None) -> ReadResponse:
		# return time of task in secs
		pass
	
	@abc.abstractmethod
	def new(self, lable, **kwargs):
		pass

	@abc.abstractmethod
	def read(self, lable) -> ReadResponse:
		# return a list that i called resp
		# resp[0] => time on this lable in secs
		# resp[1] => lable
		# resp[2] => state of this lable that can be (STOP | PROGRESS)
		pass
	
	@abc.abstractmethod
	def exists(self, lable) -> bool:
		# check existence of lable
		pass
	
	@abc.abstractmethod
	def all(self) -> [ReadResponse]:
		# return whole key and state
		pass
	
	@abc.abstractmethod
	def delete(self, lable) -> ReadResponse:
		pass
	
	@abc.abstractmethod
	def update(self, lable, key, value):
		pass
