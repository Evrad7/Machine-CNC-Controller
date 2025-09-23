import serial
import re
import time
from threading import Thread
from serial.tools import list_ports
from constantes import *
import math

# class connexion au arduino









class ConnexionArduino():
	def __init__(self,port, braudrate):
		self.port=port
		self.braudrate=braudrate
		self.recu=b""
		ports_disponibles=list_ports.comports()
		for _ in ports_disponibles:
			print(_)

		try:
			self.connexion=serial.Serial(self.port, self.braudrate)
		except:
			print("Verifier le port serie et que la console de arduino n'est pas ouverte")
			exit()
			
		print("initializing...")
		time.sleep(2)
		#print(24.encode())
		
		v="\x18".encode()# On envoie la commande Ctrl-x
		
		
		#self.recu=self.connexion.read_until().decode()
		#self.recu=self.connexion.read_until().decode()
		self.recu=self.connexion.readline().decode()
		n="\n".encode()



		print(self.recu)
		#self.connexion.write(b"\r\n\r\n")
		self.recu=self.connexion.readline().decode()
		print ("---------------------",self.recu)
		self.connexion.write_timeout=0
		"""

		
		time.sleep(2)
		self.connexion.flushInput()
		self.connexion.write("X0Y2\n".encode())
		#time.sleep(1)
		self.connexion.write("X9Z3\n".encode())
		commande="G4P0.01\n".encode()
		self.connexion.write(commande)
		for _ in range(3):
			self.recu=self.connexion.readline().decode()
			print (_, self.recu)
			


		for i in range(2):
			time.sleep(0.2)
			self.connexion.write("?".encode())
		time.sleep(5)
		print(self.connexion.inWaiting())
		self.connexion.flush()
		r=self.connexion.read(self.connexion.inWaiting()).decode().strip()
		print("r-----------------", r)


		
		for _ in range(2):
			
			print(_, self.connexion.readline().decode())

			


		r=self.connexion.write("?".encode())
		print(r)
		r=self.connexion.write("X0Y2\n".encode())
		print(r)
		#out=self.connexion.out_waiting()
		#print("outWaiting()-------", out)

	def write(self, data):
		l=input()
		try:
			l=int(l)
		except:
			print(data, l)
			return self.write(data)

		self.connexion.write("?".encode())
	
		r=self.connexion.write("X0Y2\n".encode())
		for _ in range(2):
			r=self.connexion.readline().decode()
			print(_, r)
			"""

		while False:
			
			print(self.connexion.isOpen())
			time.sleep(2)
			l=self.connexion.write("\n".encode())
			print(l, "fffffffffffffffffffffffffffffffffffff")

			r=self.connexion.readline().decode().strip()
			print(r)
			raise(serial.SerialTimeoutException)




		











		
		
		
		self.connexion.close()


		

c=ConnexionArduino("COM31", 115200)	
def conversionTemps(temps):
	secondes=temps
	if secondes<60:
		return(tronquerDec(secondes))
	if (secondes>=60 and secondes<3600):
		minutes=secondes//60
		secondes=secondes-minutes*60
		return str(minutes)+"min: "+tronquerDec(secondes)+" sec"
	if secondes>=3600:
		heures=secondes//3600
		secondes=secondes-heures*3600
		if secondes<60:	
			return str(heures)+"h: "+tronquerDec(secondes)+" s"
		if (secondes>=60 and secondes<3600):
			minutes=secondes//60
			secondes=secondes-minutes*60
			return str(heures)+"h: "+str(minutes)+" min: "+tronquerDec(secondes)+" s"

def tronquerDec(n):

	n=str(n)


	index=n.find(".")
	print(index)
	
	if index>=0:
		return n[:index+3]
	return n
while(True):
	t=input("=> ")
	t=float(t)
	print(conversionTemps(t))



#self.conneion.read(ser.inWaiting) => lire les données dans le port serie tant que quelque chose y a été ecrit 