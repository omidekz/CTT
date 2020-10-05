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
    
    def write(self, lable, time=None):
        if not time:
            time = dt.now()
        if self.data.get(lable, None):
            data = self.data.get(lable)[-1]
            self.data[lable].append({
                "time": time,
                "state": abstracts
                            .STATES
                            .value(
                                not data.get('state')
                            )
            })
        else:
            self.data[lable] = [
                {
                    "time": time,
                    "state": abstracts.STATES.PROGRESS
                }
            ]
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
        self._update_db()
    
    def read(self, lable, raise_error=False):
        self._update_data()
        if self.exists(lable):
            data = self.data[lable]
            whole = 0
            tmp_a = 0
            tmp_b = 0
            last_progress_calc = False
            for i in range(len(data)):
                if i % 2 == 0:
                    # state is PROGRESS
                    tmp_a = data[i]['time'].timestamp()
                else:
                    # state is END
                    tmp_b = data[i]['time'].timestamp()
                    whole += (tmp_b - tmp_a)
 
            if len(data) % 2 == 1:
                whole += (
                    dt.now().timestamp() 
                    - data[-1]['time'].timestamp()
                )

            return [int(whole), lable, abstracts.STATES.str(data[-1]['state'])]
        if raise_error:
            raise Exception("No Lable Exist")
    
    def exists(self, lable):
        return bool(self.data.get(lable, None))
