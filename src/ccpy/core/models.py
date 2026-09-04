"""Data contracts for the ccpy core pipeline.

Plain data only. No Qt, no I/O, no stage logic.
"""

from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ConversionJob:
    """Immutable user request for one conversion run."""

    source_dir: Path
    output_dir: Path
    overwrite: bool = False
    zip_theme: bool = False
    install_theme: bool = False
    map_file: Path | None = None


@dataclass(frozen=True)
class CursorResult:
    """Outcome of a single cursor in the finished theme."""

    name: str
    ok: bool
    error: str | None = None


@dataclass
class JobResult:
    """Final report of a run, accumulated as stages complete."""

    ok: bool
    theme_dir: Path | None = None
    archive: Path | None = None
    installed: bool = False
    cursor_results: list[CursorResult] = []


class CcpyError(Exception):
    """Base for expected core failures shown to the user, not as a traceback."""


class CursorMapError(CcpyError):
    """The cursor map is malformed and cannot be used."""


class CursorMap(Mapping[str, tuple[str, ...]]):
    """Immutable map of asset names to the Linux cursor names they serve.

    Values are normalized from space separated strings to tuples. Empty
    entries and duplicate targets raise CursorMapError at construction.
    """

    def __init__(self, entries: Mapping[str, object]) -> None:
        normalized: dict[str, tuple[str, ...]] = {}
        target_origin: dict[str, str] = {}
        for asset, raw in entries.items():
            if not isinstance(asset, str) or not asset.strip():
                raise CursorMapError(f"Invalid asset name in cursor map: {asset!r}")
            if not isinstance(raw, str):
                raise CursorMapError(
                    f"Value for asset '{asset}' must be a string, got {type(raw).__name__}"
                )
            names = tuple(raw.split())
            if not names:
                raise CursorMapError(f"Asset '{asset}' maps to no cursor names")
            for name in names:
                if name in target_origin:
                    raise CursorMapError(
                        f"Duplicate cursor target '{name}', claimed by both "
                        f"'{target_origin[name]}' and '{asset}'"
                    )
                target_origin[name] = asset
            normalized[asset] = names
        self._entries = normalized

    def __getitem__(self, key: str) -> tuple[str, ...]:
        return self._entries[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._entries)

    def __len__(self) -> int:
        return len(self._entries)

    def __repr__(self) -> str:
        return f"CursorMap({self._entries!r})"
