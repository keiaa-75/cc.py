from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class ConversionJob:
    source_dir: Path
    output_dir: Path
    overwrite: bool = False
    zip_theme: bool = False
    install_theme: bool = False
    map_file: Path | None = None

@dataclass(frozen=True)
class CursorResult:
    name: str
    ok: bool
    error: str | None = None

@dataclass
class JobResult:
    ok: bool
    theme_dir: Path | None = None
    archive: Path | None = None
    installed: bool = False
    cursor_results: list[CursorResult] = []