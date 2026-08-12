from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Local Image Search")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("homeTitle")

        subtitle = QLabel("Search local images")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setObjectName("homeSubtitle")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search images...")
        self.search_input.setMinimumHeight(46)
        self.search_input.setMaximumWidth(680)
        self.search_input.setObjectName("homeSearch")

        search_row = QHBoxLayout()
        search_row.addStretch()
        search_row.addWidget(self.search_input)
        search_row.addStretch()

        layout.addStretch(2)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addLayout(search_row)
        layout.addStretch(3)