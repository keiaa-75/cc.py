import subprocess
import shutil
import os
import sys
import json
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal

class CursorConverterLogic(QObject):
    status_update = pyqtSignal(str)
    finished = pyqtSignal(bool)

    FILES = [
        "Alternate", "Busy", "Diagonal1", "Diagonal2", "Handwriting", "Help", 
        "Horizontal", "Link", "Move", "Normal", "Person", "Pin", 
        "Precision", "Text", "Unavailable", "Vertical", "Working"
    ]
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.venv_path = Path.home() / '.venvs/win2xcur-env'
        self.cursor_map = {}

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
            
            if not self.check_dependencies(): return
            if not self.setup_python_env(): return
            if not self.load_cursor_map(map_file_path): return
            if not self.check_files(source_dir): return
            self.initial_conversion(source_dir, dest_dir)
            self.copy_assets(dest_dir)
            self.initial_conversion_cleanup(dest_dir)
            self.build_theme_files(dest_dir)
            
            if zip_theme:
                self.zip_theme(dest_dir)
            if install_theme:
                self.install_theme(dest_dir)

            self.status_update.emit("Conversion process completed successfully!")
            self.finished.emit(True)

        except Exception as e:
            self.status_update.emit(f"An unexpected error occurred: {e}")
            self.finished.emit(False)

    def check_dependencies(self):
        self.status_update.emit("Checking dependencies...")
        
        required_cmds = ['pip', 'python3', 'wget', 'zip']
        missing_cmds = [cmd for cmd in required_cmds if shutil.which(cmd) is None]

        if missing_cmds:
            self.status_update.emit(f"Error: The following commands are not installed: {', '.join(missing_cmds)}")
            return False
        
        try:
            subprocess.run([sys.executable, '-m', 'ensurepip', '--version'], 
                           check=True, 
                           capture_output=True, 
                           text=True)
        except subprocess.CalledProcessError:
            self.status_update.emit("Error: ensurepip is NOT available. Please check if python3-venv is installed.")
            return False
            
        self.status_update.emit("All dependencies are met.")
        return True
    
    def setup_python_env(self):
        self.status_update.emit("Setting up Python virtual environment...")
        
        if not self.venv_path.exists():
            try:
                subprocess.run([sys.executable, '-m', 'venv', str(self.venv_path)], 
                               check=True, 
                               capture_output=True)
            except subprocess.CalledProcessError as e:
                self.status_update.emit(f"Failed to create virtual environment: {e.stderr.strip()}")
                return False

        venv_python = str(self.venv_path / 'bin' / 'python3')
        
        self.status_update.emit("Installing/checking win2xcur...")
        try:
            subprocess.run([venv_python, '-m', 'pip', 'install', 'win2xcur'], 
                           check=True, 
                           capture_output=True)
        except subprocess.CalledProcessError as e:
            self.status_update.emit(f"Failed to install win2xcur: {e.stderr.strip()}")
            return False

        self.status_update.emit("Python environment is ready.")
        return True

    def load_cursor_map(self, map_file_path):
        """Loads cursor mapping from a JSON file and validates its content."""
        self.status_update.emit("Loading cursor mapping from file...")
        try:
            with open(map_file_path, 'r') as f:
                self.cursor_map = json.load(f)
            
            self.status_update.emit("Validating cursor map content...")
            
            # 1. Check if all required files have a corresponding key
            for f in self.FILES:
                if f not in self.cursor_map:
                    self.status_update.emit(f"Error: Missing required cursor map entry for '{f}'.")
                    return False
            
            for key, value in self.cursor_map.items():
                if not isinstance(value, str):
                    self.status_update.emit(f"Error: The value for key '{key}' is not a string. Found type: {type(value).__name__}.")
                    return False
            
            self.status_update.emit("Cursor mapping loaded and validated successfully.")
            return True
            
        except FileNotFoundError:
            self.status_update.emit(f"Error: Cursor map file '{map_file_path}' not found.")
            return False
        except json.JSONDecodeError as e:
            self.status_update.emit(f"Error: Failed to parse JSON from '{map_file_path}'. Please check the file's format. Details: {e}")
            return False

    def check_files(self, source_dir):
        self.status_update.emit("Checking for required files...")
        
        for f in self.FILES:
            if not (source_dir / f"{f}.cur").exists() and not (source_dir / f"{f}.ani").exists():
                self.status_update.emit(f"Missing file: {source_dir / f} (.cur or .ani)")
                return False
        
        self.status_update.emit("All required files are present.")
        return True

    def initial_conversion(self, source_dir, dest_dir):
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

    def copy_assets(self, dest_dir):
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

    def initial_conversion_cleanup(self, dest_dir):
        self.status_update.emit("Cleaning up intermediate files...")
        for f in self.FILES:
            intermediate_file = dest_dir / f
            if intermediate_file.exists():
                intermediate_file.unlink()
        self.status_update.emit("Cleanup complete.")

    def build_theme_files(self, dest_dir):
        self.status_update.emit("Building theme files...")
        theme_name = dest_dir.name
        
        cursor_theme_content = f"[Icon Theme]\nName={theme_name}\n"
        index_theme_content = f"[Icon Theme]\nName={theme_name}\nComment=Linux cursor theme converted by ColorCursor.\n"

        (dest_dir / 'cursor.theme').write_text(cursor_theme_content)
        (dest_dir / 'index.theme').write_text(index_theme_content)
        self.status_update.emit("Theme files created.")
    
    # -------------------- NEW METHODS --------------------
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