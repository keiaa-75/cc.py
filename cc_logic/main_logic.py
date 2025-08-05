import shutil
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal

from .dependencies import DependenciesManager
from .conversion import CursorConverter
from .theme_builder import ThemeBuilder
from .utilities import Utilities

class CursorConverterLogic(QObject):
    status_update = pyqtSignal(str)
    finished = pyqtSignal(bool)
    progress_update = pyqtSignal(int) # Add the new progress signal

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.dependencies_manager = DependenciesManager(self)
        self.converter = CursorConverter(self.dependencies_manager.venv_path, self)
        self.theme_builder = ThemeBuilder(self)
        self.utilities = Utilities(self)
        
        self.dependencies_manager.status_update.connect(self.status_update)
        self.converter.status_update.connect(self.status_update)
        self.theme_builder.status_update.connect(self.status_update)
        self.utilities.status_update.connect(self.status_update)

    def run_conversion(self, source_path, destination_path, map_file_path, zip_theme, install_theme):
        self.status_update.emit("Starting conversion process...")
        
        # ... (logging messages)
        
        try:
            source_dir = Path(source_path)
            dest_dir = Path(destination_path)
            
            # --- Progress Step 1 ---
            self.progress_update.emit(5)
            # ... (initial checks and directory setup)
            if not source_dir.is_dir():
                self.status_update.emit(f"Error: Source directory '{source_path}' does not exist.")
                self.finished.emit(False)
                return

            if dest_dir.exists():
                shutil.rmtree(dest_dir)

            dest_dir.mkdir(parents=True)

            # --- Progress Step 2 ---
            self.progress_update.emit(10)
            if not self.dependencies_manager.check_system_dependencies(): return
            if not self.dependencies_manager.setup_python_env(): return
            
            # --- Progress Step 3 ---
            self.progress_update.emit(25)
            if not self.theme_builder.load_cursor_map(map_file_path, self.converter.FILES): return
            if not self.converter.check_source_files(source_dir): return
            
            # --- Progress Step 4 ---
            self.progress_update.emit(40)
            self.converter.convert_files(source_dir, dest_dir)
            
            # --- Progress Step 5 ---
            self.progress_update.emit(60)
            self.theme_builder.copy_assets(dest_dir)
            
            # --- Progress Step 6 ---
            self.progress_update.emit(75)
            self.converter.cleanup_intermediate_files(dest_dir)
            
            # --- Progress Step 7 ---
            self.progress_update.emit(85)
            self.theme_builder.build_theme_files(dest_dir)
            
            # --- Progress Step 8 ---
            if zip_theme:
                self.progress_update.emit(90)
                self.utilities.zip_theme(dest_dir)
            if install_theme:
                self.progress_update.emit(95)
                self.utilities.install_theme(dest_dir)
            
            # --- Final Progress Step ---
            self.status_update.emit("Conversion process completed successfully!")
            self.progress_update.emit(100)
            self.finished.emit(True)

        except Exception as e:
            self.status_update.emit(f"An unexpected error occurred: {e}")
            self.progress_update.emit(0)
            self.finished.emit(False)