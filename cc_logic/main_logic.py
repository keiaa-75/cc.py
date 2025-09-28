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
    progress_update = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.dependencies_manager = DependenciesManager(self)
        self.converter = None 
        self.theme_builder = ThemeBuilder(self)
        self.utilities = Utilities(self)
        
        self.dependencies_manager.status_update.connect(self.status_update)
        self.theme_builder.status_update.connect(self.status_update)
        self.utilities.status_update.connect(self.status_update)
        
        self.source_path = ""
        self.destination_path = ""
        self.map_file_path = ""
        self.zip_theme = False
        self.install_theme = False
    
    def set_conversion_parameters(self, source_path, destination_path, map_file_path, zip_theme, install_theme):
        self.source_path = source_path
        self.destination_path = destination_path
        self.map_file_path = map_file_path
        self.zip_theme = zip_theme
        self.install_theme = install_theme

    def run_conversion(self):
        self.status_update.emit("Starting conversion process...")
        self.status_update.emit(f"Source directory: {self.source_path}")
        self.status_update.emit(f"Destination directory: {self.destination_path}")
        
        try:
            source_dir = Path(self.source_path)
            dest_dir = Path(self.destination_path)
            
            self.progress_update.emit(5)
            if dest_dir.exists():
                shutil.rmtree(dest_dir)

            dest_dir.mkdir(parents=True)

            self.progress_update.emit(10)
            if not self.dependencies_manager.check_system_dependencies(): 
                self.finished.emit(False)
                return
            if not self.dependencies_manager.setup_python_env(): 
                self.finished.emit(False)
                return
            
            self.converter = CursorConverter(self.dependencies_manager.win2xcur_path, self)
            self.converter.status_update.connect(self.status_update)

            self.progress_update.emit(25)
            if not self.theme_builder.load_cursor_map(self.map_file_path, self.converter.FILES): 
                self.finished.emit(False)
                return
            if not self.converter.check_source_files(source_dir): 
                self.finished.emit(False)
                return
            
            self.progress_update.emit(40)
            self.converter.convert_files(source_dir, dest_dir)

            self.progress_update.emit(60)
            self.theme_builder.copy_assets(dest_dir)

            self.progress_update.emit(75)
            self.converter.cleanup_intermediate_files(dest_dir)

            self.progress_update.emit(85)
            self.theme_builder.build_theme_files(dest_dir)

            if self.zip_theme:
                self.progress_update.emit(90)
                self.utilities.zip_theme(dest_dir)
            if self.install_theme:
                self.progress_update.emit(95)
                self.utilities.install_theme(dest_dir)

            self.status_update.emit("Conversion process completed successfully!")
            self.progress_update.emit(100)
            self.finished.emit(True)

        except Exception as e:
            self.status_update.emit(f"An unexpected error occurred: {e}")
            self.progress_update.emit(0)
            self.finished.emit(False)