# cc.py

[![Download cc.py](https://img.shields.io/badge/Download-Release-4285F4?style=flat&logo=github&logoColor=white)](https://github.com/keiaa-75/cc.py/releases)
[![Python](https://img.shields.io/badge/Made%20with-Python-4285F4.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Qt](https://img.shields.io/badge/Made%20with-Qt-41CD52.svg?style=flat&logo=qt&logoColor=white)](https://www.qt.io/)
[![Linux](https://img.shields.io/badge/Supports-Linux-FCC624.svg?style=flat&logo=linux&logoColor=white)](https://www.linux.org/)

**cc.py** is a user-friendly GUI tool designed to convert Windows cursor themes (`.cur` and `.ani` files) into a format compatible with Linux desktop environments.

![cc.py running on my desktop](program-screenshot.png)

This application provides a graphical interface for converting cursors using the `win2xcur` command-line utility.

It began as a simple bash script inspired by a forum request from `safeusernameig` to convert Project Sekai cursors for Linux Mint, and has since evolved into a modular Python application built with PyQt6.

## Prerequisites

To run this application, you need to have the following installed on your Linux system:

- **Python 3:** The application is built with Python 3.
- `pip` and `venv`: This is used to manage Python packages and create a virtual environment.
- `ImageMagick`: This is required by win2xcur for processing the cursor files.
- `zip`: This is the command-line utility used for zipping files. It is typically included with your Linux distribution.


## Building from Source

To build the application from source, follow these steps:

1. Clone the repository and navigate to the project directory
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application directly:
   ```bash
   python cc_ui.py
   ```
5. Build the executable (optional):
   ```bash
   pyinstaller ccpy.spec
   ```
   
The executable will be created in the `dist/` directory.


## Configuration

The application uses a JSON file to define how Windows cursors are mapped to Linux cursors. A default mapping file is included with the application.

To use a custom mapping, you may provide your own JSON file with the appropriate cursor mappings. The format expects each Windows cursor name as a key with the corresponding Linux cursor names as a space-separated string value.


## License

This project is licensed under the [Creative Commons CC0 1.0 Universal (CC0 1.0)](LICENSE). This means the software is dedicated to the public domain and is provided "as-is" without warranty of any kind. The author(s) disclaim all liability for damages resulting from the use of this software. You are free to use, modify, and distribute the software for any purpose without restriction.