import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QRubberBand

class ScreenshotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Screenshot and Crop App")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.capture_button = QPushButton("Capture Screen", self)
        self.capture_button.clicked.connect(self.capture_screen)
        layout.addWidget(self.capture_button)

        self.crop_button = QPushButton("Crop Image", self)
        self.crop_button.clicked.connect(self.crop_image)
        self.crop_button.setDisabled(True)
        layout.addWidget(self.crop_button)

        self.image_label = QLabel("No Image Captured", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.rubber_band = None
        self.start_pos = None
        self.image = None

    def capture_screen(self):
        screen = QApplication.primaryScreen()
        self.image = screen.grabWindow(0).toImage()
        pixmap = QPixmap.fromImage(self.image)
        self.image_label.setPixmap(pixmap)
        self.crop_button.setDisabled(False)

    def crop_image(self):
        if self.image:
            self.image_label.mousePressEvent = self.start_selection
            self.image_label.mouseReleaseEvent = self.end_selection
            self.image_label.mouseMoveEvent = self.track_selection
            self.rubber_band = QRubberBand(QRubberBand.Rectangle, self.image_label)
            self.image_label.setCursor(Qt.CrossCursor)

    def start_selection(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos()
            self.rubber_band.setGeometry(QRect(self.start_pos, QSize()))
            self.rubber_band.show()

    def track_selection(self, event):
        if self.rubber_band and self.start_pos:
            rect = QRect(self.start_pos, event.pos()).normalized()
            self.rubber_band.setGeometry(rect)

    def end_selection(self, event):
        if event.button() == Qt.LeftButton and self.rubber_band:
            rect = self.rubber_band.geometry()
            cropped = self.image.copy(rect)
            self.image_label.setPixmap(QPixmap.fromImage(cropped))
            self.rubber_band.hide()
            self.rubber_band.deleteLater()
            self.rubber_band = None
            self.image_label.setCursor(Qt.ArrowCursor)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ScreenshotApp()
    main_window.show()
    sys.exit(app.exec())
