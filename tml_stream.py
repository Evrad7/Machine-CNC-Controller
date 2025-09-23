import serial
from threading import Thread
from serial.tools import list_ports




def recherchePort():
		ports=list_ports.comports()
		return ports







class Connexion():
	def __init__(self, port, baudrate):
		self.port=port
		self.baudrate=baudrate
		self.enConnexion=False
		self.erreur=False


	def connecter(self):
		try:
			self.enConnexion=True
			self.connexion=serial.Serial(self.port, self.baudrate)
		except:
			self.erreur=True
		finally:
		    self.enConnexion=False	
		    







		

		