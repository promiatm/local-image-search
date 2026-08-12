import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIRECTORY = PROJECT_ROOT / "data"

def main():
    app = QApplication()

    window = MainWindow(data_directory=DATA_DIRECTORY)
    window.show()

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
