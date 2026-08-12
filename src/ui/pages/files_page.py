from pathlib import Path

from PySide6.QtCore import QDir, QSize, Qt, QTimer, QUrl
from PySide6.QtGui import QIcon, QImageReader, QPixmap
from PySide6.QtWidgets import (
    QFileSystemModel,
    QHBoxLayout,
    QLabel,
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

        self.pending_images = []
        self.thumbnail_cache = {}

        self.load_timer = QTimer(self)
        self.load_timer.timeout.connect(self.load_next_image)

        self.directory_label = QLabel()
        self.status_label = QLabel()

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.folder_tree)
        splitter.addWidget(self.gallery)
        splitter.setSizes([250, 750])

        layout = QVBoxLayout(self)
        header_layout = QHBoxLayout()
        header_layout.addWidget(self.directory_label, stretch=1)
        header_layout.addWidget(self.status_label)

        layout.addLayout(header_layout)
        layout.addWidget(splitter, stretch=1)

    def select_directory(self, index):
        directory = Path(self.folder_model.filePath(index))

        if directory.is_dir():
            self.current_directory = directory
            self.load_images()

    def load_images(self):
        # Stop loading the previous folder
        self.load_timer.stop()

        self.gallery.clear()
        self.directory_label.setText(str(self.current_directory))

        self.pending_images = sorted(
             (
                  path
                  for path in self.current_directory.iterdir()
                  if path.is_file()
                  and path.suffix.lower() in IMAGE_EXTENSIONS
             ),
             key=lambda path: path.name.lower(),
             reverse=True,
        )

        total = len(self.pending_images)
        self.status_label.setText(f"Loading 0 of {total} images")

        if total > 0:
            self.load_timer.start(0)
        else:
            self.status_label.setText("0 images")

    def load_next_image(self):
        if not self.pending_images:
            self.load_timer.stop()
            self.status_label.setText(f"{self.gallery.count()} images")
            return

        path = self.pending_images.pop()

        modified_time = path.stat().st_mtime
        cache_key = str(path)

        cached = self.thumbnail_cache.get(cache_key)

        if cached is not None:
            cached_time, cached_thumbnail = cached

            if cached_time == modified_time:
                self.add_thumbnail(path, cached_thumbnail)
                return

        reader = QImageReader(str(path))
        original_size = reader.size()

        if not original_size.isValid():
            return

        thumbnail_size = original_size.scaled(
            QSize(160, 120),
            Qt.AspectRatioMode.KeepAspectRatio,
        )

        reader.setScaledSize(thumbnail_size)
        image = reader.read()

        if image.isNull():
            return

        thumbnail = QPixmap.fromImage(image)

        self.thumbnail_cache[cache_key] = (
            modified_time,
            thumbnail,
        )

        self.add_thumbnail(path, thumbnail)

    def add_thumbnail(self, path: Path, thumbnail: QPixmap):
        item = QListWidgetItem(QIcon(thumbnail), path.name)

        item.setData(
            Qt.ItemDataRole.UserRole,
            str(path),
        )

        self.gallery.addItem(item)

        loaded = self.gallery.count()
        total = loaded + len(self.pending_images)

        self.status_label.setText(f"Loading {loaded} of {total} images")