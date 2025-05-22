import threading
import time
from enum import StrEnum, auto

from src.thread_supervisor import ThreadSupervisor
from src.run_method_type import RunMethodType

class ThreadManager:
    def __init__(self, plc_connections):

        self.plc_connections = plc_connections

        self.halt_threads = False
        self.threads_done = True
        self.stop = False

        self.supervisors = []
        self.supervisors.append(ThreadSupervisor(plc_connections=self.plc_connections,run_method_type=RunMethodType.COLLECT_DATA))
        self.supervisors.append(ThreadSupervisor(plc_connections=self.plc_connections,run_method_type=RunMethodType.CHECK_PLC_CONN))

    def start(self):
        t = threading.Thread(target=self.run, daemon=True)
        t.start()

    def run(self):

        while not self.stop:

            if not self.halt_threads:
                for s in self.supervisors:
                    s.halt_threads = False
                    s.create_worker_threads()
                self.threads_done = False
            else:
                for s in self.supervisors:
                    s.halt_threads = True

            time.sleep(0.5)

    def all_threads_done(self):
        for s in self.supervisors:
            if not s.threads_done():
                return False

        return True








