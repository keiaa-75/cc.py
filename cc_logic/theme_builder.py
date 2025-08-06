import json
import shutil
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal

class ThemeBuilder(QObject):
    status_update = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cursor_map = {}

    def load_cursor_map(self, map_file_path, required_files):
        """Loads and validates cursor mapping from a JSON file."""
        self.status_update.emit("Loading cursor mapping from file...")
        try:
            with open(map_file_path, 'r') as f:
                self.cursor_map = json.load(f)
            
            self.status_update.emit("Validating cursor map content...")
            
            for f in required_files:
                if f not in self.cursor_map:
                    self.status_update.emit(f"Error: Missing required cursor map entry for '{f}'.")
                    return False
            
            for key, value in self.cursor_map.items():
                if not isinstance(value, str):
                    self.status_update.emit(f"Error: The value for key '{key}' is not a string. Found type: {type(value).__name__}.")
                    return False
            
            self.status_update.emit("Cursor mapping loaded and validated successfully.")
            return True
        except json.JSONDecodeError as e:
            self.status_update.emit(f"Error: Failed to parse JSON from '{map_file_path}'. Please check the file's format. Details: {e}")
            return False

    def copy_assets(self, dest_dir):
        """Creates symbolic links for the converted cursors."""
        self.status_update.emit("Copying and linking cursor assets...")
        cursor_dir = dest_dir / 'cursors'
        cursor_dir.mkdir(exist_ok=True)
        
        for asset, cursor_names in self.cursor_map.items():
            source_file = dest_dir / asset
            if not source_file.exists():
                self.status_update.emit(f"Warning: Converted file '{asset}' not found. Skipping links.")
                continue

            for cursor_name in cursor_names.split():
                dest_file = cursor_dir / cursor_name
                shutil.copy2(source_file, dest_file)
        self.status_update.emit("Assets successfully copied and linked.")

    def build_theme_files(self, dest_dir):
        """Creates the cursor.theme and index.theme files."""
        self.status_update.emit("Building theme files...")
        theme_name = dest_dir.name
        
        cursor_theme_content = f"[Icon Theme]\nName={theme_name}\n"
        index_theme_content = f"[Icon Theme]\nName={theme_name}\nComment=Linux cursor theme converted by ColorCursor.\n"

        (dest_dir / 'cursor.theme').write_text(cursor_theme_content)
        (dest_dir / 'index.theme').write_text(index_theme_content)
        self.status_update.emit("Theme files created.")