# thread_executor.py

from concurrent.futures import ThreadPoolExecutor, Future
from collections.abc import Callable
from typing import Any

class ThreadExecutor:
    def __init__(self, max_workers: int=4):
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    def submit(self, function: Callable[..., Any], *args) -> Future:
        return self._executor.submit(function, *args)

    def shutdown(self) -> None:
        self._executor.shutdown(wait=False)
        