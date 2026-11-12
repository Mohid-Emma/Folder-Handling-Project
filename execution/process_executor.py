# process_executor.py

from concurrent.futures import ProcessPoolExecutor

class ProcessExecutor:
    def __init__(self):
        self.process_pool = ProcessPoolExecutor(max_workers=2)

    def submit(self, function, *args):
        return self.process_pool.submit(function, *args)

    def shutdown(self):
        self.process_pool.shutdown(wait=False)