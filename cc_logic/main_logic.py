import shutil
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal

# Import the new modules
from .dependencies import DependenciesManager
from .conversion import CursorConverter
from .theme_builder import ThemeBuilder
from .utilities import Utilities

class CursorConverterLogic(QObject):
    status_update = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Instantiate the modular classes
        self.dependencies_manager = DependenciesManager(self)
        self.converter = CursorConverter(self.dependencies_manager.venv_path, self)
        self.theme_builder = ThemeBuilder(self)
        self.utilities = Utilities(self)
        
        # Connect signals from all modules to the main status_update signal
        self.dependencies_manager.status_update.connect(self.status_update)
        self.converter.status_update.connect(self.status_update)
        self.theme_builder.status_update.connect(self.status_update)
        self.utilities.status_update.connect(self.status_update)

    def run_conversion(self, source_path, destination_path, map_file_path, zip_theme, install_theme):
        self.status_update.emit("Starting conversion process...")
        self.status_update.emit(f"Source directory: {source_path}")
        self.status_update.emit(f"Destination directory: {destination_path}")
        self.status_update.emit(f"Cursor map file: {map_file_path}")
        self.status_update.emit(f"Zip theme: {'Yes' if zip_theme else 'No'}")
        self.status_update.emit(f"Install theme: {'Yes' if install_theme else 'No'}")

        try:
            source_dir = Path(source_path)
            dest_dir = Path(destination_path)
            
            if not source_dir.is_dir():
                self.status_update.emit(f"Error: Source directory '{source_path}' does not exist.")
                self.finished.emit(False)
                return

            if dest_dir.exists():
                self.status_update.emit(f"Warning: Destination directory '{destination_path}' already exists. It will be overwritten.")
                shutil.rmtree(dest_dir)

            dest_dir.mkdir(parents=True)
            
            # Run the steps in order, calling methods from the modular classes
            if not self.dependencies_manager.check_system_dependencies(): return
            if not self.dependencies_manager.setup_python_env(): return
            if not self.theme_builder.load_cursor_map(map_file_path, self.converter.FILES): return
            if not self.converter.check_source_files(source_dir): return
            self.converter.convert_files(source_dir, dest_dir)
            self.theme_builder.copy_assets(dest_dir)
            self.converter.cleanup_intermediate_files(dest_dir)
            self.theme_builder.build_theme_files(dest_dir)
            
            if zip_theme:
                self.utilities.zip_theme(dest_dir)
            if install_theme:
                self.utilities.install_theme(dest_dir)

            self.status_update.emit("Conversion process completed successfully!")
            self.finished.emit(True)

        except Exception as e:
            self.status_update.emit(f"An unexpected error occurred: {e}")
            self.finished.emit(False)