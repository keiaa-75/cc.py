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
        self.venv_python_path = None
        self.win2xcur_path = None
        self.system_python_path = None

    def _find_system_python(self):
        """Finds the system's Python interpreter path."""
        # Try to find python3, then fall back to python
        python_path = shutil.which('python3')
        if python_path is None:
            python_path = shutil.which('python')
        
        if python_path is None:
            self.status_update.emit("Error: Could not find a system Python interpreter.")
            return False
        
        self.system_python_path = python_path
        return True

    def check_system_dependencies(self):
        """Checks if required command-line tools are installed."""
        self.status_update.emit("Checking system dependencies...")
        
        if not self._find_system_python():
            return False
            
        required_cmds = ['pip', 'wget', 'zip']
        missing_cmds = [cmd for cmd in required_cmds if shutil.which(cmd) is None]

        if missing_cmds:
            self.status_update.emit(f"Error: The following commands are not installed: {', '.join(missing_cmds)}")
            return False
        
        try:
            # Use the found system Python interpreter to check for ensurepip
            subprocess.run([self.system_python_path, '-m', 'ensurepip', '--version'], 
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
                # Use the system's Python to create the venv, not sys.executable
                subprocess.run([self.system_python_path, '-m', 'venv', str(self.venv_path)], 
                               check=True, 
                               capture_output=True)
            except subprocess.CalledProcessError as e:
                self.status_update.emit(f"Failed to create virtual environment: {e.stderr.strip()}")
                return False

        # Determine the correct path to the venv's Python interpreter
        if sys.platform == 'win32':
            venv_bin_path = self.venv_path / 'Scripts'
            venv_python_exe = venv_bin_path / 'python.exe'
        else:
            venv_bin_path = self.venv_path / 'bin'
            venv_python_exe = venv_bin_path / 'python'

        self.venv_python_path = str(venv_python_exe)

        if not Path(self.venv_python_path).exists():
            self.status_update.emit(f"Error: Virtual environment Python executable not found at {self.venv_python_path}.")
            return False

        self.status_update.emit("Installing/checking win2xcur...")
        try:
            # Use the venv's Python for pip
            subprocess.run([self.venv_python_path, '-m', 'pip', 'install', 'win2xcur'], 
                           check=True, 
                           capture_output=True)
        except subprocess.CalledProcessError as e:
            self.status_update.emit(f"Failed to install win2xcur: {e.stderr.strip()}")
            return False

        # Find the win2xcur executable explicitly
        if sys.platform == 'win32':
            win2xcur_exe_path = venv_bin_path / 'win2xcur.exe'
        else:
            win2xcur_exe_path = venv_bin_path / 'win2xcur'
            
        if not win2xcur_exe_path.exists():
            self.win2xcur_path = shutil.which('win2xcur', path=str(venv_bin_path))
        else:
            self.win2xcur_path = str(win2xcur_exe_path)

        if not self.win2xcur_path:
            self.status_update.emit("Error: win2xcur executable not found in the virtual environment.")
            return False

        self.status_update.emit("Python environment is ready.")
        return True