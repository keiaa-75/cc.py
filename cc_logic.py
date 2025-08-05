import subprocess
import shutil
import os
import sys
from PyQt6.QtCore import QObject, pyqtSignal

class CursorConverterLogic(QObject):
    # Define custom signals for communication with the GUI
    status_update = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)

    def run_conversion(self, source_path, destination_path):
        """Main method to orchestrate the entire conversion process."""
        self.status_update.emit("Starting conversion process...")
        self.status_update.emit(f"Source directory: {source_path}")
        self.status_update.emit(f"Destination directory: {destination_path}")

        # You would call other methods here to perform the full conversion
        if self.check_dependencies():
            self.status_update.emit("All dependencies are met.")
            # We'll add the rest of the logic here in future steps
        else:
            self.status_update.emit("Dependencies check failed. Aborting.")
        
        self.finished.emit()

    def check_dependencies(self):
        """
        Checks if required command-line tools are installed.
        Returns True if all dependencies are met, False otherwise.
        """
        self.status_update.emit("Checking dependencies...")
        
        required_cmds = ['pip', 'python3', 'wget', 'zip']
        missing_cmds = []

        for cmd in required_cmds:
            if shutil.which(cmd) is None:
                missing_cmds.append(cmd)

        if missing_cmds:
            self.status_update.emit(f"Error: The following commands are not installed: {', '.join(missing_cmds)}")
            return False
        
        # Check for ensurepip, which is a key part of your script's logic
        try:
            # `python3 -m ensurepip` will fail if the venv module is not available
            subprocess.run([sys.executable, '-m', 'ensurepip', '--version'], 
                           check=True, 
                           capture_output=True, 
                           text=True)
        except subprocess.CalledProcessError:
            self.status_update.emit("Error: ensurepip is NOT available. Please check if python3-venv is installed.")
            return False
            
        return True