# cc.py

[![Download cc.py](https://img.shields.io/badge/Download-Release-blue?style=for-the-badge&logo=github)](https://github.com/keiaa-75/cc.py/releases)
[![Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Qt](https://img.shields.io/badge/Made%20with-Qt-41CD52.svg?style=for-the-badge&logo=qt)](https://www.qt.io/)
[![Linux](https://img.shields.io/badge/Supports-Linux-FCC624.svg?style=for-the-badge&logo=linux)](https://www.linux.org/)

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