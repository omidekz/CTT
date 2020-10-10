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
	
	def __repr__(self):
		return str(self)
