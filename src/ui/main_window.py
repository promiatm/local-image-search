from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ui.pages.home_page import HomePage
from ui.pages.files_page import FilesPage

class PlaceholderPage(QWidget):
    def __init__(self, title):
        super().__init__()

        layout = QVBoxLayout(self)

        label = QLabel(f"{title}\n\nComing later")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setObjectName("emptyLabel")

        layout.addWidget(label)

class MainWindow(QMainWindow):
    def __init__(self, data_directory: Path):
        super().__init__()

        self.setWindowTitle("Local Image Search")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        self.resize(1920, 1080)

        centralWidget = QWidget()
        root_layout = QHBoxLayout(centralWidget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(240)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 24, 16, 16)

        application_name = QLabel("Local Image\nSearch")
        application_name.setObjectName("applicationName")

        self.navigation = QListWidget()
        self.navigation.setObjectName("navigation")
        self.navigation.addItems(
            [
                "Home",
                "Search",
                "People",
                "Files",
                "Settings",
            ]
        )
        self.navigation.setSpacing(4)
        self.navigation.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        sidebar_layout.addWidget(application_name)
        sidebar_layout.addSpacing(24)
        sidebar_layout.addWidget(self.navigation, stretch=1)

        self.pages = QStackedWidget()
        self.pages.addWidget(HomePage())
        self.pages.addWidget(PlaceholderPage("Search"))
        self.pages.addWidget(PlaceholderPage("People"))
        self.pages.addWidget(FilesPage(data_directory))
        self.pages.addWidget(PlaceholderPage("Settings"))

        self.navigation.currentRowChanged.connect(
            self.pages.setCurrentIndex
        )

        root_layout.addWidget(sidebar)
        root_layout.addWidget(self.pages, stretch=1)

        self.setCentralWidget(centralWidget)
        self.apply_styles()

        self.navigation.setCurrentRow(0)

    def apply_styles(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow {
                background: #f6f7f9;
            }

            QFrame#sidebar {
                background: #ffffff;
                border-right: 1px solid #dcdfe4;
            }

            QLabel#applicationName {
                color: #172033;
                font-size: 18px;
                font-weight: 700;
            }

            QListWidget#navigation {
                background: transparent;
                border: none;
                outline: none;
                color: #3b4354;
                font-size: 14px;
            }

            QListWidget#navigation::item {
                min-height: 40px;
                padding-left: 12px;
                border-radius: 6px;
            }

            QListWidget#navigation::item:hover {
                background: #eef2f7;
            }

            QListWidget#navigation::item:selected {
                background: #dfeaff;
                color: #1859b5;
                font-weight: 600;
            }

            QLabel#homeTitle {
                color: #172033;
                font-size: 32px;
                font-weight: 700;
            }

            QLabel#homeSubtitle {
                color: #6b7280;
                font-size: 15px;
            }

            QLineEdit#homeSearch {
                background: #ffffff;
                border: 1px solid #cdd2da;
                border-radius: 22px;
                padding: 0 20px;
                font-size: 15px;
            }

            QLineEdit#homeSearch:focus {
                border: 2px solid #3977d6;
            }

            QLabel#pageTitle {
                color: #172033;
                font-size: 24px;
                font-weight: 700;
            }

            QLabel#statusLabel {
                color: #6b7280;
            }

            QLabel#emptyLabel {
                color: #7a8290;
                font-size: 15px;
            }

            QListView {
                background: #ffffff;
                border: 1px solid #dcdfe4;
                border-radius: 8px;
                padding: 12px;
            }

            QListView::item {
                padding: 6px;
                border-radius: 6px;
            }

            QListView::item:hover {
                background: #eef2f7;
            }

            QListView::item:selected {
                background: #dfeaff;
                color: #172033;
            }

            QPushButton {
                background: #ffffff;
                border: 1px solid #cdd2da;
                border-radius: 6px;
                padding: 7px 14px;
            }

            QPushButton:hover {
                background: #eef2f7;
            }
            """
        )