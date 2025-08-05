import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QFileDialog, QCheckBox)
from PyQt6.QtCore import Qt
from pathlib import Path

from cc_logic import CursorConverterLogic

class CursorConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.logic = CursorConverterLogic()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ColorCursor Converter')
        self.setFixedSize(600, 500) # Increased the height for new widgets
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)

        layout = QVBoxLayout()

        source_label = QLabel('Source Directory:')
        self.source_path_input = QLineEdit()
        self.source_path_input.setPlaceholderText('Enter path to source directory...')
        self.source_browse_button = QPushButton('Browse')
        self.source_browse_button.clicked.connect(self.browse_source_directory)
        layout.addWidget(source_label)
        layout.addWidget(self.source_path_input)
        layout.addWidget(self.source_browse_button)

        destination_label = QLabel('Destination Directory:')
        self.destination_path_input = QLineEdit()
        self.destination_path_input.setPlaceholderText('Enter path to destination directory...')
        self.destination_browse_button = QPushButton('Browse')
        self.destination_browse_button.clicked.connect(self.browse_destination_directory)
        layout.addWidget(destination_label)
        layout.addWidget(self.destination_path_input)
        layout.addWidget(self.destination_browse_button)
        
        map_label = QLabel('Cursor Map File (.json):')
        self.map_file_input = QLineEdit()
        default_map_path = str(Path(__file__).parent / "cursor_map.json")
        self.map_file_input.setText(default_map_path)
        self.map_file_input.setPlaceholderText('Enter path to cursor map JSON file...')
        
        self.map_browse_button = QPushButton('Browse')
        self.map_browse_button.clicked.connect(self.browse_map_file)
        
        layout.addWidget(map_label)
        layout.addWidget(self.map_file_input)
        layout.addWidget(self.map_browse_button)

        self.zip_checkbox = QCheckBox('Zip theme?')
        self.install_checkbox = QCheckBox('Install theme?')
        
        layout.addWidget(self.zip_checkbox)
        layout.addWidget(self.install_checkbox)

        self.convert_button = QPushButton('Start Conversion')
        self.convert_button.clicked.connect(self.start_conversion_process)
        layout.addWidget(self.convert_button)

        status_label = QLabel('Status Log:')
        self.status_log = QTextEdit()
        self.status_log.setReadOnly(True)
        
        layout.addWidget(status_label)
        layout.addWidget(self.status_log)

        self.logic.status_update.connect(self.update_status_log)
        self.logic.finished.connect(self.conversion_finished)

        self.setLayout(layout)

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

    def start_conversion_process(self):
        source_path = self.source_path_input.text()
        destination_path = self.destination_path_input.text()
        map_file_path = self.map_file_input.text()
        
        zip_theme = self.zip_checkbox.isChecked()
        install_theme = self.install_checkbox.isChecked()
        
        self.status_log.clear()
        
        self.convert_button.setEnabled(False)
        self.source_browse_button.setEnabled(False)
        self.destination_browse_button.setEnabled(False)
        self.map_browse_button.setEnabled(False)
        self.zip_checkbox.setEnabled(False)
        self.install_checkbox.setEnabled(False)

        self.logic.run_conversion(source_path, destination_path, map_file_path, zip_theme, install_theme)

    def update_status_log(self, message):
        self.status_log.append(message)

    def conversion_finished(self, success):
        if success:
            self.status_log.append("Conversion process finished successfully!")
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