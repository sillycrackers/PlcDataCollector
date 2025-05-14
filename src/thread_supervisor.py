import threading

import src.plc_connection
from src.worker_thread import WorkerThread
from src.run_method_type import RunMethodType

class ThreadSupervisor:
    def __init__(self, plc_connections, run_method_type : RunMethodType):

        self.plc_connections = plc_connections
        self.run_method_type = run_method_type
        self.threads = {}
        self.halt_threads = False

        #status dict used to track the state of each thread
        #if the state is False then it is ready to start again
        self.status = {}
        self.lock = threading.Lock()

    def create_worker_threads(self):

        #Populate status dict with current plc connections
        self.populate_status_dict()

        element_to_delete = ''

        ''' 
        loop through status dict, remove item if no longer in plc 
        connections, otherwise if status False, 
        create a new thread for that connection and start it
        '''

        for status_name in self.status:
            if status_name in self.plc_connections:
                if self.status[status_name] == False:

                    t = WorkerThread(name=status_name, run_method=self.run_method, done_method=self.done_callback)
                    t.start()

                    self.lock.acquire()
                    self.status[status_name] = True
                    self.lock.release()
            else:
                element_to_delete = status_name

        if element_to_delete:
            del self.status[element_to_delete]

    def done_callback(self, name):
        self.lock.acquire()
        self.status[name] = False
        self.lock.release()

    def run_method(self, name):

        while not self.halt_threads:

            if self.run_method_type == RunMethodType.COLLECT_DATA:
                self.plc_connections[name].collect_data()
            elif self.run_method_type == RunMethodType.CHECK_PLC_CONN:
                self.plc_connections[name].check_plc_connection()
            else:
                raise Exception("missing/invalid run method type for thread")

    def threads_done(self):

        self.lock.acquire()
        for status_name in self.status:
            if self.status[status_name]:
                self.lock.release()

                return False
        self.lock.release()


        return True

    def populate_status_dict(self):
        for con in self.plc_connections:
            if con not in self.status:
                self.status[con] = False
