import shutil
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal

class Utilities(QObject):
    status_update = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
    
    def zip_theme(self, dest_dir):
        """Zips the theme directory."""
        self.status_update.emit("Zipping theme...")
        try:
            shutil.make_archive(dest_dir, 'zip', root_dir=dest_dir.parent, base_dir=dest_dir.name)
            self.status_update.emit(f"Successfully zipped theme to {dest_dir}.zip")
        except Exception as e:
            self.status_update.emit(f"Failed to zip theme: {e}")

    def install_theme(self, dest_dir):
        """Installs the theme by copying it to ~/.icons/."""
        self.status_update.emit("Installing theme...")
        try:
            icons_dir = Path.home() / '.icons'
            icons_dir.mkdir(parents=True, exist_ok=True)
            
            shutil.copytree(dest_dir, icons_dir / dest_dir.name, dirs_exist_ok=True)
            self.status_update.emit(f"Successfully installed theme to {icons_dir / dest_dir.name}")
        except Exception as e:
            self.status_update.emit(f"Failed to install theme: {e}")