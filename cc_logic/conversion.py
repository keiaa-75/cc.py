import subprocess
import os
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal

class CursorConverter(QObject):
    status_update = pyqtSignal(str)
    
    FILES = [
        "Alternate", "Busy", "Diagonal1", "Diagonal2", "Handwriting", "Help", 
        "Horizontal", "Link", "Move", "Normal", "Person", "Pin", 
        "Precision", "Text", "Unavailable", "Vertical", "Working"
    ]
    
    def __init__(self, venv_path, parent=None):
        super().__init__(parent)
        self.venv_path = venv_path

    def check_source_files(self, source_dir):
        """Checks for the presence of all required cursor files."""
        self.status_update.emit("Checking for required files...")
        
        for f in self.FILES:
            if not (source_dir / f"{f}.cur").exists() and not (source_dir / f"{f}.ani").exists():
                self.status_update.emit(f"Missing file: {source_dir / f} (.cur or .ani)")
                return False
        
        self.status_update.emit("All required files are present.")
        return True

    def convert_files(self, source_dir, dest_dir):
        """Converts Windows cursors to Linux format using win2xcur."""
        self.status_update.emit("Starting initial cursor conversion...")
        
        win2xcur_path = str(self.venv_path / 'bin' / 'win2xcur')
        
        for f in self.FILES:
            input_file = (source_dir / f"{f}.cur") if (source_dir / f"{f}.cur").exists() else (source_dir / f"{f}.ani")
            self.status_update.emit(f"Converting {input_file.name}...")
            try:
                subprocess.run([win2xcur_path, str(input_file), '-o', str(dest_dir)], 
                               check=True, 
                               capture_output=True)
            except subprocess.CalledProcessError as e:
                self.status_update.emit(f"Conversion failed for {input_file.name}: {e.stderr.strip()}")
                raise e

    def cleanup_intermediate_files(self, dest_dir):
        """Removes the intermediate converted files."""
        self.status_update.emit("Cleaning up intermediate files...")
        for f in self.FILES:
            intermediate_file = dest_dir / f
            if intermediate_file.exists():
                intermediate_file.unlink()
        self.status_update.emit("Cleanup complete.")