import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QFileDialog)
from PyQt6.QtCore import Qt

# Import our new logic class
from cc_logic import CursorConverterLogic

class CursorConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        # Create an instance of our logic class
        self.logic = CursorConverterLogic()
        self.initUI()

    def initUI(self):
        # ... (rest of initUI is the same as before)
        self.setWindowTitle('ColorCursor Converter')
        self.setFixedSize(600, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)

        layout = QVBoxLayout()
        # ... (source and destination directory widgets)
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

        # -------------------- Conversion Button --------------------
        self.convert_button = QPushButton('Start Conversion')
        # Connect the convert button to our new method
        self.convert_button.clicked.connect(self.start_conversion_process)
        layout.addWidget(self.convert_button)

        # -------------------- Status Log Widgets --------------------
        status_label = QLabel('Status Log:')
        self.status_log = QTextEdit()
        self.status_log.setReadOnly(True)
        
        layout.addWidget(status_label)
        layout.addWidget(self.status_log)

        # Connect the logic's signals to our GUI's slots
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

    # -------------------- NEW METHODS --------------------
    def start_conversion_process(self):
        """This method will be triggered by the 'Start Conversion' button."""
        source_path = self.source_path_input.text()
        destination_path = self.destination_path_input.text()
        
        self.status_log.clear() # Clear the log for a new run
        
        # Disable buttons to prevent user from starting multiple processes
        self.convert_button.setEnabled(False)
        self.source_browse_button.setEnabled(False)
        self.destination_browse_button.setEnabled(False)

        # Call the logic class to begin the work
        self.logic.run_conversion(source_path, destination_path)

    def update_status_log(self, message):
        """A slot to receive messages from the logic and add them to the log."""
        self.status_log.append(message)

    def conversion_finished(self):
        """A slot to be executed when the logic class signals completion."""
        self.status_log.append("Conversion process finished.")
        # Re-enable the buttons
        self.convert_button.setEnabled(True)
        self.source_browse_button.setEnabled(True)
        self.destination_browse_button.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CursorConverterApp()
    ex.show()
    sys.exit(app.exec())