
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon

class ButtonG55 (QPushButton):
	def __init__(self, parent=None):

		super(ButtonG55, self).__init__(parent)
		self.quitte=True


	def enterEvent(self, event):
		self.setIcon(QIcon("images/G55E.PNG"))

		
		
	def leaveEvent(self, event):
		if self.quitte:
			self.setIcon(QIcon("images/G55.PNG"))
		
		

	

	

