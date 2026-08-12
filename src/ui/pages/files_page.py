from pathlib import Path

from PySide6.QtCore import QDir, QSize, Qt, QUrl
from PySide6.QtGui import QIcon, QImageReader, QPixmap
from PySide6.QtWidgets import (
    QFileSystemModel,
    QListView,
    QListWidget,
    QListWidgetItem,
    QSplitter,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
}

class FilesPage(QWidget):
    def __init__(self, data_directory: Path):
        super().__init__()

        data_directory.mkdir(parents=True, exist_ok=True)

        self.data_directory = data_directory.resolve()
        self.current_directory = self.data_directory

        self.folder_model = QFileSystemModel(self)
        self.folder_model.setFilter(
            QDir.Filter.AllDirs | QDir.Filter.NoDotAndDotDot
        )

        data_index = self.folder_model.setRootPath(
            str(self.data_directory)
        )

        self.folder_tree = QTreeView()
        self.folder_tree.setModel(self.folder_model)
        self.folder_tree.setRootIndex(data_index)
        self.folder_tree.clicked.connect(self.select_directory)

        self.gallery = QListWidget()
        self.gallery.setViewMode(QListView.IconMode)
        self.gallery.setResizeMode(QListView.ResizeMode.Adjust)
        self.gallery.setMovement(QListView.Movement.Static)
        self.gallery.setIconSize(QSize(160, 120))
        self.gallery.setGridSize(QSize(190, 165))
        self.gallery.setSpacing(8)
        self.gallery.setWordWrap(True)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.folder_tree)
        splitter.addWidget(self.gallery)
        splitter.setSizes([250, 750])

        layout = QVBoxLayout(self)
        layout.addWidget(splitter)

        self.load_images()

    def select_directory(self, index):
        directory = Path(self.folder_model.filePath(index))

        if directory.is_dir():
            self.current_directory = directory
            self.load_images()

    def load_images(self):
        self.gallery.clear()

        for path in self.current_directory.iterdir():
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:

                reader = QImageReader(str(path))
                original_size = reader.size()

                if not original_size.isValid():
                    continue

                thumbnail_size = original_size.scaled(
                    QSize(160, 120),
                    Qt.AspectRatioMode.KeepAspectRatio,
                )

                reader.setScaledSize(thumbnail_size)
                image = reader.read()

                if image.isNull():
                    continue

                thumbnail = QPixmap.fromImage(image)

                item = QListWidgetItem(QIcon(thumbnail), path.name)
                self.gallery.addItem(item)