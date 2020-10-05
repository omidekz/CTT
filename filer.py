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
    
    def write(self, lable, time=None, **kwargs):
        if not time:
            time = dt.now()
        if not self.data.get(lable, False):
            self.data[lable] = []

        data = self.data[lable]
        state = data[-1]['state'] if len(data) > 0 \
                                else abstracts.STATES.END
        self.data[lable].append({
            "time": time,
            "state": not state,
            "kwargs": kwargs
        })

        self.stop_all_except(lable, update_db=False)
        self._update_db()
    
    def stop_all_except(self, lable, update_db=True):
        for loop_lable, data in self.data.items():
            if lable == loop_lable:
                continue
            if abstracts \
                .STATES \
                .is_progress(data[-1]['state']):
                data.append({
                    "time": time,
                    "state": abstracts.STATES.END
                })
            self.data[loop_lable] = data
        
        if update_db:
            self._update_db()
    
    def _calc_time(self, record):
        whole = 0
        tmp_a = 0
        tmp_b = 0
        last_progress_calc = False
        for i in range(len(record)):
            if i % 2 == 0:
                # state is PROGRESS
                tmp_a = record[i]['time'].timestamp()
            else:
                # state is END
                tmp_b = record[i]['time'].timestamp()
                whole += (tmp_b - tmp_a)

        if len(record) % 2 == 1:
            whole += (
                dt.now().timestamp() 
                - record[-1]['time'].timestamp()
            )
        
        return whole
    
    def read(self, lable, raise_error=False):
        self._update_data()
        if self.exists(lable):
            data = self.data[lable]
            
            whole_time = self._calc_time(data)

            return [int(whole_time), lable, abstracts.STATES.str(data[-1]['state'])]
        if raise_error:
            raise Exception("No Lable Exist")
    
    def exists(self, lable):
        return bool(self.data.get(lable, None))
    
    def all(self):
        def cb(item):
            lable = item[0]
            data = item[1]
            return lable, abstracts.STATES.str(data[-1]['state'])
        return list(map(cb, self.data.items()))

    def delete(self, lable):
        result = self.data.pop(lable, None)
        self._update_db()
        return result