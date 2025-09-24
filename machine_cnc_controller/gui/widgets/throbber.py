"""Loading animation displayed while stopping the machine."""

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QLabel

from machine_cnc_controller.resources import image_path


class Throbber(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        label = QLabel(self)
        label.setText("Arrêt en cours ...")

        self.setWindowTitle("")
        self.resize(100, 100)
        self.setFixedSize(self.width(), self.height())
        self.setStyleSheet("background-color:white;")
        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        newflags = Qt.Dialog
        newflags |= Qt.CustomizeWindowHint
        newflags &= ~Qt.WindowCloseButtonHint
        newflags &= ~Qt.WindowSystemMenuHint
        newflags &= ~Qt.WindowContextHelpButtonHint
        self.setWindowFlags(newflags)

        self.movie = QMovie(image_path("ajax-loader.gif"))
        self.movie.setScaledSize(QSize(40, 40))
        self.setMovie(self.movie)
        self.movie.start()

    def closeEvent(self, event):
        self.movie.stop()
        self.clear()
        event.accept()
