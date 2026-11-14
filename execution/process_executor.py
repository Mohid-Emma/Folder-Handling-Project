# process_executor.py

from concurrent.futures import ProcessPoolExecutor, Future
from collections.abc import Callable
from typing import Any

class ProcessExecutor:
    def __init__(self, max_workers: int=4) -> None:
        self.process_pool = ProcessPoolExecutor(max_workers)

    def submit(self, function: Callable[..., Any], *args) -> Future:
        return self.process_pool.submit(function, *args)

    def shutdown(self) -> None:
        self.process_pool.shutdown(wait=False)