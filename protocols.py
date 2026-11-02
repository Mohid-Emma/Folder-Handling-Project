# protocols.py

from typing import Protocol, Any, TypedDict
from collections.abc import Callable



# =============================================================
# Frontend Protocol
# =============================================================

PlanItem = dict[str, Any]
FormData = dict[str, Any]

PreviewCallback = Callable[
    [str, FormData], list[PlanItem | None] ]

ExecuteCallback = Callable[[str], None]


class ControllerCallbacks(TypedDict):
    preview: PreviewCallback
    execute: ExecuteCallback

# =============================================================
# Backend Protocol
# =============================================================

class PlanProvider(Protocol):
    plan: list[dict[str, Any]]

    def create_plan(self) -> list[dict[str, Any]]:
        ...

class PlanExecuter(Protocol):
    plan: list[dict[str, Any]]

    def execute_plan(self) -> list[dict[str, Any]]:
        ...