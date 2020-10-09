import os.path
from datetime import datetime as dt
import pickle
import abstracts

class Manager(abstracts.BaseManager):
    def __init__(self, db_path):
        super().__init__(db_path)
        if not os.path.exists(self.db_path):
            self.data = {}
            self._update_db()

        self._update_data()
    
    def _update_db(self):
        file = open(self.db_path, 'wb')
        pickle.dump(self.data, file)
        file.close()
    
    def _update_data(self):
        file = open(self.db_path, 'rb')
        self.data = pickle.load(file)
        file.close()
    
    def is_inprogress(self, times):
        return len(times) % 2 == 1

    def toggle(self, lable, time=None):
        if not self.exists(lable):
            return None
        
        if not time:
            time = dt.now()

        self.data[lable]['times'].append(time)
        
        if self.is_inprogress(self.data[lable]['times']):
            self.stop_all_except(lable, update_db=False)
        self._update_db()
        
        return self._to_readresponse(lable, self.data[lable])
    
    def _to_readresponse(self, lable, data):
        return abstracts.ReadResponse(
            lable,
            whole_time=self._calc_time(data),
            times=data['times'],
            **data['kwargs']
        )

    def new(self, lable, **kwargs):
        self.data[lable] = {
            "times": [],
            "kwargs": kwargs
        }
        self._update_db()
        return self._to_readresponse(lable, self.data[lable])

    def stop_all_except(self, lable, update_db=True):
        for loop_lable, data in self.data.items():
            if lable == loop_lable:
                continue
            if self.is_inprogress(data['times']):
                data['times'].append(dt.now())
            self.data[loop_lable] = data
        
        if update_db:
            self._update_db()
    
    def _calc_time(self, record):
        whole = 0
        tmp_a = 0
        tmp_b = 0
        times = record['times']
        for i in range(len(times)):
            if i % 2 == 0:
                # its a start time
                tmp_a = record[i].timestamp()
            else:
                # its end time
                tmp_b = record[i].timestamp()
                whole += (tmp_b - tmp_a)

        if self.is_inprogress(times):
            # task is in progress
            whole += (
                dt.now().timestamp() 
                - record[-1].timestamp() # the last start time of task
            )
        
        return whole # whole time of task
    
    def read(self, lable, raise_error=False):
        self._update_data()
        if self.exists(lable):
            data = self.data[lable]
            return self._to_readresponse(lable, data)
        if raise_error:
            raise Exception("No Lable Exist")
    
    def exists(self, lable):
        return bool(self.data.get(lable, None))
    
    def all(self):
        def cb(item):
            lable = item[0]
            data = item[1]
            return self._to_readresponse(lable, data)
        return list(map(cb, self.data.items()))

    def delete(self, lable):
        result = self.data.pop(lable, None)
        if result:
            self._update_db()
            return self._to_readresponse(lable, result)
    
    def rename(self, old, new):
        if self.exists(old):
            data = self.data.pop(old)
            self.data[new] = data
            self._update_db()
    
    def update(self, lable, key, value):
        if self.exists(lable):
            self.data[lable]['kwargs']['key'] = value
            self._update_db()
