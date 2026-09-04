"""Event contract shared by all core stages.

Stages emit small immutable events through an injected reporter.
The GUI worker and the CLI are the only consumers.
No other UI related imports here.
"""

from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class CoreEvent:
    stage: str
    message: str

@dataclass(frozen=True)
class ProgressEvent:
    stage: str
    message: str
    index: int | None = None
    total: int | None = None

@dataclass(frozen=True)
class FailureEvent(CoreEvent):
    """Fatal error in the named stage. The run stops, then cleans up."""

@dataclass(frozen=True)
class CleanupEvent(CoreEvent):
    """Partial output was removed after a failure."""
    path: str = ""

class ProgressReporter(Protocol):
    """Callable that receives core events. 
    Implemented by the GUI worker and the CLI.
    """
    def __call__(self, event: ProgressEvent) -> None: ...

class NullReporter:
    """Discards events. Used in tests and headless runs."""
    def __call__(self, event: ProgressEvent) -> None:
        pass