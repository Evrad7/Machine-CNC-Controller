"""Loading animation displayed while stopping the machine."""

from pathlib import Path

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QLabel


class Throbber(QLabel):
    def __init__(self, parent=None):
        image = Path(__file__).resolve().parents[2] / "ajax-loader.gif"
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

        self.movie = QMovie(str(image))
        self.movie.setScaledSize(QSize(40, 40))
        self.setMovie(self.movie)
        self.movie.start()

    def closeEvent(self, event):
        self.movie.stop()
        self.clear()
        event.accept()
