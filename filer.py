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
    
    def write(self, lable, time):
        if not time:
            time = dt.now()
        if self.data.get(lable, None):
            data = self.data.get(lable)[-1]
            self.data.append({
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
        self._update_db()
    
    def read(self, lable, raise_error=False):
        self._update_data()
        if self.exists(lable):
            data = self.data[lable]
            return [-1, lable, abstracts.STATES.str(data[-1]['state'])]
        if raise_error:
            raise Exception("No Lable Exist")
    
    def exists(self, lable):
        return bool(self.data.get(lable, None))
