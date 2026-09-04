from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class ProgressEvent:
    stage: str
    message: str
    index: int | None = None
    total: int | None = None

class ProgressReporter(Protocol):
    def __call__(self, event: ProgressEvent) -> None: ...

class NullReporter:
    def __call__(self, event: ProgressEvent) -> None:
        pass