import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QFileDialog, QSizePolicy)
from PyQt6.QtCore import Qt

class CursorConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the main window properties
        self.setWindowTitle('ColorCursor Converter')
        self.setFixedSize(600, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)
        layout = QVBoxLayout()

        # -------------------- Source Directory Widgets --------------------
        source_label = QLabel('Source Directory:')
        self.source_path_input = QLineEdit()
        self.source_path_input.setPlaceholderText('Enter path to source directory...')
        
        source_browse_button = QPushButton('Browse')
        
        layout.addWidget(source_label)
        layout.addWidget(self.source_path_input)
        layout.addWidget(source_browse_button)

        # -------------------- Destination Directory Widgets --------------------
        destination_label = QLabel('Destination Directory:')
        self.destination_path_input = QLineEdit()
        self.destination_path_input.setPlaceholderText('Enter path to destination directory...')

        destination_browse_button = QPushButton('Browse')

        layout.addWidget(destination_label)
        layout.addWidget(self.destination_path_input)
        layout.addWidget(destination_browse_button)

        # -------------------- Conversion Button --------------------
        convert_button = QPushButton('Start Conversion')
        layout.addWidget(convert_button)

        # -------------------- Status Log Widgets --------------------
        status_label = QLabel('Status Log:')
        self.status_log = QTextEdit()
        self.status_log.setReadOnly(True) # Make the text edit read-only
        
        layout.addWidget(status_label)
        layout.addWidget(self.status_log)

        # Set the main layout for the window
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CursorConverterApp()
    ex.show()
    sys.exit(app.exec())