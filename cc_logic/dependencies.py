import subprocess
import shutil
import sys
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal

class DependenciesManager(QObject):
    status_update = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.venv_path = Path.home() / '.venvs/win2xcur-env'

    def check_system_dependencies(self):
        """Checks if required command-line tools are installed."""
        self.status_update.emit("Checking system dependencies...")
        
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
            
        self.status_update.emit("All system dependencies are met.")
        return True

    def setup_python_env(self):
        """Creates a virtual environment and installs win2xcur."""
        self.status_update.emit("Setting up Python virtual environment...")
        
        if not self.venv_path.exists():
            try:
                subprocess.run([sys.executable, '-m', 'venv', str(self.venv_path)], 
                               check=True, 
                               capture_output=True)
            except subprocess.CalledError as e:
                self.status_update.emit(f"Failed to create virtual environment: {e.stderr.strip()}")
                return False

        venv_python = str(self.venv_path / 'bin' / 'python3')
        
        self.status_update.emit("Installing/checking win2xcur...")
        try:
            subprocess.run([venv_python, '-m', 'pip', 'install', 'win2xcur'], 
                           check=True, 
                           capture_output=True)
        except subprocess.CalledError as e:
            self.status_update.emit(f"Failed to install win2xcur: {e.stderr.strip()}")
            return False

        self.status_update.emit("Python environment is ready.")
        return True