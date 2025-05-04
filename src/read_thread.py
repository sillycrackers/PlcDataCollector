import threading


class ReadThread(threading.Thread):
    def __init__(self, name, run_method, done_method):
        threading.Thread.__init__(self)

        self.daemon = True
        self.name = name
        self.run_method = run_method
        self.done_method = done_method


    def run(self):
        print(f"{self.name} starting")
        self.run_method(self.name)
        self.done_method(self.name)