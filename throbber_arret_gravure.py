from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QSize, pyqtSlot, pyqtSignal, QThread
import os

class Throbber(QLabel):
	def __init__(self, parent=None):
		image=os.path.abspath("ajax-loader.gif")
		super(Throbber, self).__init__(parent)
		label=QLabel(self)
		label.setText("Arrêt en cours ...")
	
		self.setWindowTitle("")
		self.resize(100, 100)
		self.setFixedSize(self.width(), self.height())
		self.setStyleSheet("background-color:white;")
		self.setAlignment(Qt.AlignHCenter| Qt.AlignVCenter)
		newflags=Qt.Dialog
		newflags|=Qt.CustomizeWindowHint
		newflags&=~Qt.WindowCloseButtonHint
		newflags&=~Qt.WindowSystemMenuHint
		newflags&=~Qt.WindowContextHelpButtonHint
		self.setWindowFlags(newflags)

		self.movie=QMovie(image)
		self.movie.setScaledSize(QSize(40, 40))
		self.setMovie(self.movie)
		self.movie.start()

	def closeEvent(self, event):
		self.movie.stop()
		self.clear()
		event.accept()
