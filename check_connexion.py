from threading import Thread
from PyQt5.QtCore import pyqtSignal 
import time

class CheckConnexion(Thread):
	
	def __init__(self, connexion):
		super(CheckConnexion, self).__init__()
		self.connexion=connexion
		#self.signalStop=pyqtSignal(bool)

		def run(self):
			while self.connexion.isOpen():
				time.sleep(0.05)
				print(self.connexion.isOpen())

			#raise(NameError)
			#self.signalStop.emit(True)

	

