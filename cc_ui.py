import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QFileDialog)
from PyQt6.QtCore import Qt

from cc_logic import CursorConverterLogic

class CursorConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.logic = CursorConverterLogic()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ColorCursor Converter')
        self.setFixedSize(600, 450) # Increased the height to accommodate the new input field
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)

        layout = QVBoxLayout()

        # ... (Source and Destination directory widgets remain the same)
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
        
        # -------------------- NEW WIDGETS FOR CURSOR MAP --------------------
        map_label = QLabel('Cursor Map File (.json):')
        self.map_file_input = QLineEdit()
        # Set a default path to the file in the same directory as the script
        default_map_path = str(Path(__file__).parent / "cursor_map.json")
        self.map_file_input.setText(default_map_path)
        self.map_file_input.setPlaceholderText('Enter path to cursor map JSON file...')
        
        self.map_browse_button = QPushButton('Browse')
        self.map_browse_button.clicked.connect(self.browse_map_file)
        
        layout.addWidget(map_label)
        layout.addWidget(self.map_file_input)
        layout.addWidget(self.map_browse_button)

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
        # ... (This method remains the same)
        directory = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        if directory:
            self.source_path_input.setText(directory)

    def browse_destination_directory(self):
        # ... (This method remains the same)
        directory = QFileDialog.getExistingDirectory(self, "Select Destination Directory")
        if directory:
            self.destination_path_input.setText(directory)

    def browse_map_file(self):
        """Opens a file dialog to select the cursor map JSON file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Cursor Map File", "", "JSON Files (*.json)")
        if file_path:
            self.map_file_input.setText(file_path)

    def start_conversion_process(self):
        source_path = self.source_path_input.text()
        destination_path = self.destination_path_input.text()
        map_file_path = self.map_file_input.text()
        
        self.status_log.clear()
        
        self.convert_button.setEnabled(False)
        self.source_browse_button.setEnabled(False)
        self.destination_browse_button.setEnabled(False)
        self.map_browse_button.setEnabled(False)

        # Now pass the map file path to the logic class
        self.logic.run_conversion(source_path, destination_path, map_file_path)

    def update_status_log(self, message):
        self.status_log.append(message)

    def conversion_finished(self, success):
        # ... (This method remains the same, except for the new `success` parameter)
        if success:
            self.status_log.append("Conversion process finished successfully!")
        else:
            self.status_log.append("Conversion process finished with errors.")
        
        self.convert_button.setEnabled(True)
        self.source_browse_button.setEnabled(True)
        self.destination_browse_button.setEnabled(True)
        self.map_browse_button.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CursorConverterApp()
    ex.show()
    sys.exit(app.exec())