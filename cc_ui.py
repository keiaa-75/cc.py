import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QFileDialog, QCheckBox,
                             QProgressBar, QMessageBox)
from PyQt6.QtCore import Qt, QThread
from pathlib import Path
import os

from cc_logic.main_logic import CursorConverterLogic

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class CursorConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.thread = QThread()
        self.logic = CursorConverterLogic()
        self.logic.moveToThread(self.thread)
        
        self.initUI()
        
        self.thread.started.connect(self.logic.run_conversion)
        
        self.logic.finished.connect(self.thread.quit)
        self.logic.finished.connect(self.thread.wait)
        self.logic.finished.connect(self.logic.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)


    def initUI(self):
        self.setWindowTitle('ColorCursor Converter')
        self.setFixedSize(600, 550) 
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)

        main_layout = QVBoxLayout()

        self._create_path_widgets(main_layout)
        self._create_option_widgets(main_layout)
        self._create_control_widgets(main_layout)
        self._create_status_widgets(main_layout)

        self._connect_logic_signals()

        self.setLayout(main_layout)

    def _create_path_widgets(self, layout):
        """Creates and adds the path input widgets to the layout."""
        source_label = QLabel('Source Directory:')
        self.source_path_input = QLineEdit()
        self.source_path_input.setPlaceholderText('Enter path to source directory...')
        self.source_browse_button = QPushButton('Browse')
        self.source_browse_button.clicked.connect(self.browse_source_directory)

        destination_label = QLabel('Destination Directory:')
        self.destination_path_input = QLineEdit()
        self.destination_path_input.setPlaceholderText('Enter path to destination directory...')
        self.destination_browse_button = QPushButton('Browse')
        self.destination_browse_button.clicked.connect(self.browse_destination_directory)

        map_label = QLabel('Cursor Map File (.json):')
        self.map_file_input = QLineEdit()
        
        default_map_path = resource_path("cursor_map.json")
        self.map_file_input.setText(default_map_path)
        
        self.map_file_input.setPlaceholderText('Enter path to cursor map JSON file...')
        self.map_browse_button = QPushButton('Browse')
        self.map_browse_button.clicked.connect(self.browse_map_file)

        for widget in [source_label, self.source_path_input, self.source_browse_button,
                       destination_label, self.destination_path_input, self.destination_browse_button,
                       map_label, self.map_file_input, self.map_browse_button]:
            layout.addWidget(widget)

    def _create_option_widgets(self, layout):
        """Creates and adds the checkbox option widgets to the layout."""
        self.zip_checkbox = QCheckBox('Zip theme?')
        self.install_checkbox = QCheckBox('Install theme?')
        layout.addWidget(self.zip_checkbox)
        layout.addWidget(self.install_checkbox)

    def _create_control_widgets(self, layout):
        """Creates and adds the main control buttons and progress bar."""
        self.convert_button = QPushButton('Start Conversion')
        self.convert_button.clicked.connect(self.start_conversion_process)
        layout.addWidget(self.convert_button)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

    def _create_status_widgets(self, layout):
        """Creates and adds the status log widgets."""
        status_label = QLabel('Status Log:')
        self.status_log = QTextEdit()
        self.status_log.setReadOnly(True)
        layout.addWidget(status_label)
        layout.addWidget(self.status_log)

    def _connect_logic_signals(self):
        """Connects signals from the logic worker to UI slots."""
        self.logic.status_update.connect(self.update_status_log)
        self.logic.finished.connect(self.conversion_finished)
        self.logic.progress_update.connect(self.progress_bar.setValue)

    def browse_source_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        if directory:
            self.source_path_input.setText(directory)

    def browse_destination_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Destination Directory")
        if directory:
            self.destination_path_input.setText(directory)

    def browse_map_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Cursor Map File", "", "JSON Files (*.json)")
        if file_path:
            self.map_file_input.setText(file_path)

    def _show_error_message(self, title, message):
        """Helper to display a critical error message box."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(title)
        msg.setInformativeText(message)
        msg.setWindowTitle(title)
        msg.exec()

    def _validate_inputs(self):
        """Validates all user inputs before starting the conversion."""
        source_path = self.source_path_input.text().strip()
        destination_path = self.destination_path_input.text().strip()
        map_file_path = self.map_file_input.text().strip()

        if not all([source_path, destination_path, map_file_path]):
            self._show_error_message("Validation Error", "All path fields must be filled.")
            return False

        source_dir = Path(source_path)
        dest_dir = Path(destination_path)
        map_file = Path(map_file_path)

        if not source_dir.is_dir():
            self._show_error_message("Validation Error", f"Source directory does not exist:\n{source_dir}")
            return False
        if not map_file.is_file():
            self._show_error_message("Validation Error", f"Cursor map file does not exist:\n{map_file}")
            return False

        source_res, dest_res = source_dir.resolve(), dest_dir.resolve()

        if source_res == dest_res:
            self._show_error_message("Validation Error", "Source and destination directories cannot be the same.")
            return False
        if source_res in dest_res.parents:
            self._show_error_message("Validation Error", "Destination directory cannot be a subfolder of the source directory.")
            return False

        return True

    def start_conversion_process(self):
        if not self._validate_inputs():
            return

        destination_path = self.destination_path_input.text().strip()
        msg = QMessageBox()
        msg.setWindowTitle("Confirm Conversion")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setText("Are you sure you want to start the conversion?")
        msg.setInformativeText(f"The directory '{destination_path}' and its contents will be overwritten.")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        
        reply = msg.exec()
        
        if reply == QMessageBox.StandardButton.No:
            self.status_log.append("Conversion canceled by user.")
            return

        self.convert_button.setEnabled(False)
        self.source_browse_button.setEnabled(False)
        self.destination_browse_button.setEnabled(False)
        self.map_browse_button.setEnabled(False)
        self.zip_checkbox.setEnabled(False)
        self.install_checkbox.setEnabled(False)

        self.status_log.clear()
        self.progress_bar.setValue(0)
        
        source_path = self.source_path_input.text().strip()
        map_file_path = self.map_file_input.text().strip()
        zip_theme = self.zip_checkbox.isChecked()
        install_theme = self.install_checkbox.isChecked()
        
        self.logic.set_conversion_parameters(source_path, destination_path, map_file_path, zip_theme, install_theme)
        self.thread.start()


    def update_status_log(self, message):
        self.status_log.append(message)

    def conversion_finished(self, success):
        if success:
            self.status_log.append("Conversion process finished successfully!")
            self.progress_bar.setValue(100)
        else:
            self.status_log.append("Conversion process finished with errors.")
        
        self.convert_button.setEnabled(True)
        self.source_browse_button.setEnabled(True)
        self.destination_browse_button.setEnabled(True)
        self.map_browse_button.setEnabled(True)
        self.zip_checkbox.setEnabled(True)
        self.install_checkbox.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CursorConverterApp()
    ex.show()
    sys.exit(app.exec())