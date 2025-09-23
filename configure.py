from configuration_ui import Ui_Form
from PyQt5.QtWidgets import QMainWindow

class Configuration(QMainWindow, Ui_Form):
	def __init__(self):
		super(Configuration, self).__init__()
		self.setupUi(self)
		