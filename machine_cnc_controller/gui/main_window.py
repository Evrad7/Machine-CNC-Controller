from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QAction
from PyQt5.QtCore import pyqtSlot, QCoreApplication, QRunnable, QThreadPool, Qt
from PyQt5.QtGui import QTextCursor, QIcon

import csv
import math
import os
import re
import sys
import threading
import time
from threading import Thread

from machine_cnc_controller.communication.homing import PriseOrigine
from machine_cnc_controller.communication.monitor import CheckConnexion
from machine_cnc_controller.communication.serial import Connexion, recherchePort
from machine_cnc_controller.utils.constants import TAILLE_BUFFER_RX

from .configurator import Configurateur
from .generated.main_window_ui import Ui_mainWindow
from .message_box import MessageBoxG, activerLaCase
from .reports import Rapports
from .throbber import Throbber


INTERVAL_DE_RAPPORT=1

TX=""
RAPPORTS=[]
plainTextEditConsole=[]
progressBar=[]
labelLignesRestantes=[]
labelTempsRestant=[]
labelVitesse=[]
plainTextEditCommande=[]
enPause=False

WRITING=True

class MainWindowSender( QMainWindow,  Ui_mainWindow):
	ENPAUSE=False
	ARRETER=False
	STREAMER=True
	ENACTIVITE=True# Activation rapports d'Etat
	EN_ARRET=False #Siglal pour lancer l'animation
	WCO=[0, 0, 0]
	SYNCHRONISATEUR="libre"
	ecrire=False
	def __init__(self, parent=None):

		super(MainWindowSender, self).__init__(parent)
		self.setupUi(self)
		self.move(200, 0)
		self.pushButtonConnecter.setEnabled(False)
		self.connecte=False
		self.widgetDetails.setVisible(True)
		self.progressBar.setVisible(False)
		self.pushButtonBreak.setVisible(False)
		self.pushButtonArreter.setVisible(False)
		self.enPause=False
		self.pushButtonGraverDessiner.setEnabled(False)

		self.comboBoxFeedRate.setCurrentIndex(3)
		self.comboBoxDistance.setCurrentIndex(2)
		for _ in  [self.pushButtonZ, self.pushButton_Z, self.pushButtonY, self.pushButton_Y, self.pushButtonX, self.pushButton_X]:
			_.setAutoRepeat(True)
			_.setAutoRepeatInterval(250)
		print(self.pushButtonZ.autoRepeatInterval())
		self.progressBarJog.setVisible(False)

		self.fichier=None
		self.lignes=3609
		self.x=0
		self.wco="1"
		
		self.repereActif="1"
		self.action=self.menu_Configuration.addAction("Configurer")

		self.action.triggered.connect(self.config)
		self.pushButtonBreak.clicked.connect(self.onPushButtonBreakClicked)
		self.checkBoxCommandeManuelle.setEnabled(False)
		self.throbber=None#On dédinit le throbber au debut des opérations a None
		self.fermable=True
		self.commande_rapport="?".encode()
		self.pushButtonG54.setIcon(QIcon("images/G54P.PNG"))
		activerLaCase(self)
		#self.pushButtonGraverDessiner.setEnabled(False)
		self.textEditCommande.setReadOnly(True)

	
		

		#STREAMER=True
	def stop(self):
		while True:
			print("selfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
		




		
		#self.messageBoxG.show()








	def config(self):
		if self.connecte:
			print("TML")
			self.configurateur=Configurateur(self.connexion.connexion, self.plainTextEditConsole, self.labelUnite_)
			self.configurateur.setWindowModality(Qt.ApplicationModal)
			self.configurateur.show()
			print("tml")
		else:
			QMessageBox.information(self, " ","Veillez d'abord vous connectez a la machine")


	@pyqtSlot()
	def on_textEditCommande_textChanged(self):
		texte=self.textEditCommande.toPlainText()
		print(texte)
		if texte.find("\n")>=0:
			self.connexion.connexion.write(texte.encode())
			print(self.connexion.connexion.inWaiting(), "inwaiting()")
			time.sleep(0.05)
			
			
			
			while self.connexion.connexion.inWaiting():
				print(self.connexion.connexion.inWaiting(), "inwaiting()")
				self.plainTextEditCommande.moveCursor(QTextCursor.End)
				rx=self.connexion.connexion.readline().decode()
				self.plainTextEditCommande.insertPlainText(rx)
				self.plainTextEditCommande.ensureCursorVisible()
			self.textEditCommande.clear()





		

	@pyqtSlot()
	def on_pushButtonConnecter_clicked(self):#Connexion
		if self.connecte==False:
			#print("TML")
			
			self.plainTextEditConsole.show()
		

			port=self.comboBoxPort.currentText().strip()
			baudrate=self.comboBoxBaudrate.currentText().strip()
		
			if int(baudrate)!=115200:
				QMessageBox.warning(self, "erreur", "Le Baudrate recommendé est de 115200")
				return
			try:
				baudrate=int(baudrate)#Verifie que le baudrate est un entier
			except:
				QMessageBox.information(self, "erreur baudrate", "Entrez un baudrate valide")
			else:
				self.connexion=Connexion(port, baudrate)
				
			    
				self.connexion.connecter()

				if self.connexion.erreur: #En cas d'erreur
					QMessageBox.warning(self, "echec de connexion", "verifier que le port n'est pas occupé ou est connecter et reésseyez")

				
				else:

					self.connexion.connexion.timeout=1
					self.connecte=True
					self.checkBoxCommandeManuelle.setEnabled(True)
					self.pushButtonConnecter.setText("Deconnecter")
					self.comboBoxPort.setEnabled(False)
					self.comboBoxBaudrate.setEnabled(False)
					#self.reception() # Lancement du thread
					self.plainTextEditConsole.insertPlainText("@ {} sur la port {} ....\n ".format(self.labelInformationDuMateriel.text(), self.comboBoxPort.currentText()))
					print(self.connexion.connexion.write_timeout,"----------------------------")

					#while(self.connexion.connexion.inWaiting()):
					for _ in range(4):
						rx=self.connexion.connexion.readline().decode().strip()
						self.plainTextEditConsole.insertPlainText(rx+"\n")
						print(rx)
						if rx=="[MSG:'$H'|'$X' to unlock]":
							self.connexion.connexion.write("$X\n".encode())

							#while(self.connexion.connexion.inWaiting()):
							for _ in range(2):
								rx1=self.connexion.connexion.readline().decode().strip()
								self.plainTextEditConsole.insertPlainText(rx1+"\n")



						
					#for _ in range(2):
						#self.plainTextEditConsole.insertPlainText(self.connexion.connexion.readline().decode())

					self.configurateur=Configurateur(self.connexion.connexion, self.plainTextEditConsole, self.labelUnite_)# Util pour le mode afficher les uniter(pouce/mm)
					self.connexion.connexion.timeout=None
					self.textEditCommande.setReadOnly(False)

					
			#self.threadRapport()# rapports

				


		else:
			self.connexion.connexion.close()
			self.connecte=False
			self.checkBoxCommandeManuelle.setEnabled(False)
			self.pushButtonConnecter.setText("Connecter")
			self.comboBoxPort.setEnabled(True)
			self.comboBoxBaudrate.setEnabled(True)
			self.plainTextEditConsole.insertPlainText("Connexion terminée ...")
			self.textEditCommande.setReadOnly(True)



	"""
	@pyqtSlot()
	def on_pushButtonOriginePiece_clicked(self):
		self.connexion.connexion.write("$G\n".encode())
		for _ in range(2):
			print(self.connexion.connexion.readline().decode())
		#self.__init__()
		raise(serial.SerialTimeoutException)
		"""
	@pyqtSlot()
	def on_pushButtonOriginePiece_clicked(self):
		#x=self.lcdNumberXM.value()
		#y=self.lcdNumberYM.value()
		#z=self.lcdNumberZM.value()
		if self.connecte:
			code="G92X0Y0Z0\n".encode()
			self.connexion.connexion.write(code)
			rx=self.connexion.connexion.readline().decode().strip()
			if rx!="ok":
				QMessageBox.warning(self, "erreur", "La prise d'origine à échoué")
			else:
				QMessageBox.information(self, " ", "La prise d'origine réussie")
				self.connexion.connexion.write("?".encode())
				rx=self.connexion.connexion.readline().decode().strip()
				self.affichageCoordonnees(rx)
		else:
			QMessageBox.warning(self, "Aucune connexion", "Veillez vous connecter ")









	@pyqtSlot()
	def on_pushButtonSearchPort_clicked(self):
		ports=recherchePort()
		c=self.comboBoxPort.count()
		#print(c)
		for _ in range(c):
			self.comboBoxPort.removeItem(_)# On vide la liste
		self.labelInformationDuMateriel.setText("--------------")
		self.pushButtonConnecter.setEnabled(False)

		if len(ports)>0:# S'il y'a des ports disponibles
			for _ in ports:
				self.comboBoxPort.addItem(_[0])
				self.labelInformationDuMateriel.setText(_[1])
			self.pushButtonConnecter.setEnabled(True)	
		else: # Sinon
			QMessageBox.information(self, "Aucun port ", "Aucun port Conneté. \n Veillez verifier la connexion de votre port")

	@pyqtSlot()
	def on_pushButtonImportFichier_clicked(self):
		(fichier, filtre)=QFileDialog.getOpenFileName(self, "importer un fichier", 
			                                         filter="Fichier gcode(*.gcode);;Tout(*.*)")
		if fichier:
			self.fichier=fichier
			self.lineEdit.setText(self.fichier)
			self.pushButtonGraverDessiner.setEnabled(False)

		

	@pyqtSlot()
	def on_pushButtonAfficherLesDetails_clicked(self):
		if self.widgetDetails.isVisible():
			self.widgetDetails.setVisible(False)
			self.pushButtonAfficherLesDetails.setText("Afficher les détails")
		else:
			self.widgetDetails.setVisible(True)
			self.pushButtonAfficherLesDetails.setText("Masquer les détails")



	@pyqtSlot(str)
	def on_lineEdit_textChanged(self, path):
		if len(path.strip())<1:
			self.pushButtonAnalyser.setEnabled(False)
		else:
			self.fichier=path
			self.pushButtonAnalyser.setEnabled(True)


	@pyqtSlot()
	def on_pushButtonAnalyser_clicked(self):
	    self.analyser()
	    #self.pushButtonGraverDessiner.setEnabled(True)

	def reception(self):
		if self.connecte:
			receipt=Tx(self.connexion.connexion, self.plainTextEditConsole)
			receipt.start()
		
			self.plainTextEditConsole.setPlainText(TX)



	def onPushButtonBreakClicked(self):
		if MainWindowSender.ENPAUSE:
			MainWindowSender.ENPAUSE=False
			self.pushButtonBreak.setText("Pause")
		else:
			MainWindowSender.ENPAUSE=True
			self.pushButtonBreak.setText("Continuer")


	@pyqtSlot()
	def on_pushButtonArreter_clicked(self):
		reponse=QMessageBox.question(self, "arrêt", "Voulez vous vraiment arrêter l'opération ??", QMessageBox.Yes, QMessageBox.No)
		if reponse==QMessageBox.Yes:
			MainWindowSender.ARRETER=True
			self.pushButtonBreak.setText("pause")
			self.pushButtonBreak.setEnabled(False)
			print("TML ARRETER")
			print(self.ARRETER)

	




	@pyqtSlot()
	def on_pushButtonGraverDessiner_clicked(self):
		self.threadPool=QThreadPool()
		fichier="C:JLKJLKJKLHKJLHKJHKHK"
		connexion=789798
		self.fermable=False
		self.etatStreamer(False)
		self.checkConnexion=CheckConnexion(self.connexion)
		self.checkConnexion.start()
		#self.checkConnexion.signalStop.connect(self.stop)
	
		threadConnexion=ThreadConnexion(self.fichier, self.connexion.connexion, self.lignes)
		"""

		
		thread=Thread(target=self.rapports)
		thread.daemon=True
		thread.start()
		"""
	
		
		

	
		#self.pushButtonBreak.setVisible(True)
		#self.pushButtonGraverDessiner.setEnabled(False)
		#self.pushButtonAnalyser.setEnabled(False)
	
		self.labelNombreDeLignes.setText(str(self.lignes))
		self.progressBar.setVisible(True)
		QCoreApplication.processEvents()
		self.threadPool.start(threadConnexion)

		
		#temps+=time.time()
		while MainWindowSender.STREAMER:
			if MainWindowSender.EN_ARRET:
				if self.throbber!=None:
					pass
				else:
					self.throbber=Throbber()
					self.throbber.setWindowModality(Qt.ApplicationModal)
					self.throbber.show()
	
			
		
			while MainWindowSender.ENPAUSE:
				QCoreApplication.processEvents()
			if len(plainTextEditCommande)>0:
				self.affichageCoordonnees(plainTextEditCommande[0])

				self.plainTextEditCommande.insertPlainText(plainTextEditCommande[0])
				#print(plainTextEditCommande)

				del(plainTextEditCommande[0])

					


		
		
	
		
			#print("rapports: "+str(RAPPORTS))
			if len(plainTextEditConsole)>0:
				self.plainTextEditConsole.insertPlainText(plainTextEditConsole[0])
				del(plainTextEditConsole[0])
				self.plainTextEditConsole.moveCursor(QTextCursor.End)
				self.plainTextEditConsole.ensureCursorVisible()
				QCoreApplication.processEvents()
			
			if len(progressBar)>0:
				self.progressBar.setValue(progressBar[0])
				del(progressBar[0])
				QCoreApplication.processEvents()
			
			if len(labelLignesRestantes)>0:
				self.labelLignesRestantes.setText(labelLignesRestantes[0])
				del(labelLignesRestantes[0])
				QCoreApplication.processEvents()
			
			if len(labelTempsRestant)>0:
				self.labelTempsRestant.setText(self.conversionTemps(labelTempsRestant[0]))
				del(labelTempsRestant[0])
				QCoreApplication.processEvents()
			
			if len(labelVitesse)>0:
				self.labelVitesse.setText(str(labelVitesse[0]))
				del(labelVitesse[0]) 
				QCoreApplication.processEvents()
			
			if self.enPause:
				enPause=True
			if not self.enPause:
				enPause=False
			QCoreApplication.processEvents()
		self.etatStreamer(True)
		QCoreApplication.processEvents()
		self.fermable=True

		if self.throbber!=None:
			self.throbber.close()
			self.throbber=None
			self.pushButtonBreak.setEnabled(True)

			


				
	
			



	def analyser(self):
		if  not self.connecte:
			QMessageBox.warning(self, "aucune connexion", "veillez vous connecter")
		elif self.fichier is None:
			QMessageBox.warning(self, "aucun fichier", "veillez  importer un fichier")
		else:

			self.connexion.connexion.write(b"$C\n")
			#etat=True
			rx=""
			while rx!="ok":

				print("TML")
				rx=self.connexion.connexion.readline().decode().strip()

				self.plainTextEditConsole.insertPlainText(rx+"\n")
				if rx.find("error")>=0:
					QMessageBox.information(self, "erreur", "l'activation du mode l'analyse a échoué")

			self.check()

	def affichageCoordonnees(self, rapport):
		#rapport=plainTextEditCommande[0]
		if  rapport[0]=="<":
			end_state=rapport.find("|")
			state=rapport[1:end_state]
			self.labelEtat.setText(state)

			rapport=rapport[end_state+1:]
			begin_MPos=rapport.find(":")
			end_MPos=rapport.find("|")
			Mpos=rapport[begin_MPos+1:end_MPos]
			x, y, z=Mpos.split(",")
			self.lcdNumberXM.display(float(x))
			self.lcdNumberYM.display(float(y))
			self.lcdNumberZM.display(float(z))
			rapport=rapport[end_MPos+1:]
			begin_WCO=rapport.find("WCO")
			if begin_WCO>0:
				rapport=rapport[begin_WCO+2:]
				begin_wco=rapport.find(":")
				end_wco=rapport.find(">")
				wco=rapport[begin_wco+1:end_wco]
				MainWindowSender.WCO[0], MainWindowSender.WCO[1], MainWindowSender.WCO[2]=wco.split(",")
				
			x_=float(x)-float(MainWindowSender.WCO[0])
			y_=float(y)-float(MainWindowSender.WCO[1])
			z_=float(z)-float(MainWindowSender.WCO[2])


			self.lcdNumberXT.display(x_)
			self.lcdNumberYT.display(y_)
			self.lcdNumberZT.display(z_)











	def check(self):
		
		try:
			with open(self.fichier, "r") as file:
				nombreLigne=0
				totalTemps=0
				erreurs={}# ditionnaire de rapport d'erreurr
				self.lignes=0
				for line in file:
					self.lignes+=1
				self.labelNombreDeLignes.setText(str(self.lignes))				
				print(self.lignes)
				self.connexion.connexion.flushInput()
		except FileNotFoundError:
			QMessageBox.warning(self, "erreur", "Fichier introuvable")
			return
		
		#new_fichier=open("nouveau_fichier.gcode", "w")
			


		with open(self.fichier, "r") as file:
			self.actionAnalyserCommence()




			for line in file:
				nombreLigne+=1
				code=line.strip()+"\n"
				while self.ENPAUSE:
					time.sleep(0.05)
					QCoreApplication.processEvents()
					if MainWindowSender.ARRETER:
						self.onPushButtonBreakClicked()
				if MainWindowSender.ARRETER:
					break

				temps=time.time()
				self.connexion.connexion.write(code.encode())
				etat=True
				while etat:
					tx=self.connexion.connexion.readline().decode().strip()
					if tx.find("ok")>=0:
						etat=False
						#new_fichier.write(line)
						#ssprint(tx)
					if tx.find("error")>=0:
						#erreurs[tx[6:]]=[]# utilise un try-except et intercepte l'erreur lorsque le dictionnaire n'a pas encore de clé c'est à dire une KeyError
						try:
							erreurs[tx[6:]].append(nombreLigne)

						except KeyError:
							erreurs[tx[6:]]=[]
							erreurs[tx[6:]].append(nombreLigne)
						print(tx[6:])
						etat=False
					if tx.find("MSG"):
						etat=False
					#time.sleep(0.05)
					temps=time.time()-temps
					print("temps", temps)
					if temps==0:
						temps=0.000000000001#  A revoir
					totalTemps+=temps
					tempsMoyen=totalTemps/nombreLigne
					print(tempsMoyen,"temps moyen")
					self.plainTextEditConsole.moveCursor(QTextCursor.End)# deplacer la barre où on veut scroller
					pourcentageProgression=nombreLigne*100/self.lignes
					self.labelLignesRestantes.setText(str(self.lignes-nombreLigne))
					self.progressBar.setValue(pourcentageProgression)      
					self.plainTextEditConsole.insertPlainText(str(nombreLigne)+"-"+str(code[0:len(code)-1])+": "+ tx+"\n")
					#print(temps*1000)
					self.labelVitesse.setText(str(int(1/temps)))
				
					self.labelTempsRestant.setText(self.conversionTemps(tempsMoyen*(self.lignes-nombreLigne)))
					self.plainTextEditConsole.ensureCursorVisible()# scroll it
					QCoreApplication.processEvents()# Forcer le rendu de la fenetre*
			#new_fichier.close()

			

		
		#print(erreurs)
		rapports=""
		with open("error_codes_en_US.csv", "r") as file:
			fichier_csv=csv.reader(file, delimiter=",")
			for row in fichier_csv:
				for key, value in erreurs.items():
					print(row[0])
					if int(row[0])==int(key):
						rapports+=str(row[1])+":   "+str(row[2])+ "    lignes "+str(value[:100])+"\n\n\n"
		print(rapports)
		self.connexion.connexion.write("$C\n".encode())
		rx=""
		while rx!="ok":
			rx=self.connexion.connexion.readline().decode().strip()
			self.plainTextEditConsole.insertPlainText(rx+"\n")
		self.connexion.connexion.timeout=0

		l=self.connexion.connexion.readlines()
		print(l,"llllllllllllllllllllllllllllllllllllllllllllllllll")
		self.connexion.connexion.timeout=None
		print(self.progressBar.value())
		if self.progressBar.value()==100:
			if len(rapports)>0:
				self.rap=Rapports(rapports)

				self.rap.setWindowModality(Qt.ApplicationModal)
				self.rap.show()
			else:
				QMessageBox.information(self, "rapports de l'analyse", "L'analyse s'est éfectuée sans erreur")
				self.pushButtonGraverDessiner.setEnabled(True)


		else:
			QMessageBox.warning(self, " " , "l'operation d'analyse a été interrompue")
		self.actionAnalyserFinit()




			


						
					
				



		print(nombreLigne)
		print(rapports)
		print("temps moyen" + str(totalTemps/nombreLigne))
		self.ARRETER=False


	"""def threadStreamer(self):
		thread=Thread(target=self.streamer)
		#thread.daemon=True
		thread.start()
		"""
	def actionAnalyserCommence(self):
		self.pushButtonAnalyser.setEnabled(False)
		self.progressBar.setVisible(True)
		self.pushButtonBreak.setVisible(True)
		self.pushButtonArreter.setVisible(True)
		self.pushButtonConnecter.setEnabled(False)
		self.pushButtonG54.setEnabled(False)
		self.pushButtonG55.setEnabled(False)
		self.pushButtonG56.setEnabled(False)
		self.pushButtonG57.setEnabled(False)
		self.pushButtonG58.setEnabled(False)
		self.pushButtonG59.setEnabled(False)
		self.checkBoxCommandeManuelle.setChecked(False)
		self.checkBoxCommandeManuelle.setEnabled(False)
		self.pushButtonImportFichier.setEnabled(False)
		self.pushButtonSearchPort.setEnabled(False)
		self.action.setEnabled(False)
		self.pushButtonPriseOrigine.setEnabled(False)
		self.textEditCommande.setReadOnly(True)


	def actionAnalyserFinit(self):
		self.pushButtonAnalyser.setEnabled(True)
		self.pushButtonBreak.setVisible(False)
		self.pushButtonArreter.setVisible(False)
		self.pushButtonConnecter.setEnabled(True)
		self.pushButtonG54.setEnabled(True)
		self.pushButtonG55.setEnabled(True)
		self.pushButtonG56.setEnabled(True)
		self.pushButtonG57.setEnabled(True)
		self.pushButtonG58.setEnabled(True)
		self.pushButtonG59.setEnabled(True)
		self.checkBoxCommandeManuelle.setEnabled(True)
		self.pushButtonImportFichier.setEnabled(True)
		self.pushButtonSearchPort.setEnabled(True)
		self.progressBar.setValue(0)
		self.progressBar.setVisible(False)
		self.action.setEnabled(True)
		self.pushButtonPriseOrigine.setEnabled(True)
		MainWindowSender.ARRETER=False
		self.textEditCommande.setReadOnly(False)
		

		"""
	def mouseMoveEvent(self, mouseEvent):
		if self.x<10:
			print(self.pos())

			self.pushButtonG54.setIcon(QIcon("imges/G54AP.PNG"))
			print("faittttttttttttttttttttttttttttttttttttt")
			"""
	
		
		
	
		
		






	@pyqtSlot()
	def on_pushButtonZ_pressed(self):
		print("TML")
		self.jogging("z")

	@pyqtSlot()
	def on_pushButton_Z_clicked(self):
		self.jogging("-z")
	@pyqtSlot()
	def on_pushButtonY_clicked(self):
		self.jogging("y")
	@pyqtSlot()
	def on_pushButton_Y_clicked(self):
		self.jogging("-y")
	@pyqtSlot()
	def on_pushButtonX_clicked(self):
		self.jogging("x")
	@pyqtSlot()
	def on_pushButton_X_clicked(self):
		self.jogging("-x")

	@pyqtSlot()
	def on_pushButtonRemiseAZero_clicked(self):
		print(self.x)



	def etatJogging(self, etat):
		self.pushButtonConnecter.setEnabled(etat)
		self.pushButtonSearchPort.setEnabled(etat)
		self.pushButtonG54.setEnabled(etat)
		self.pushButtonG55.setEnabled(etat)
		self.pushButtonG56.setEnabled(etat)
		self.pushButtonG57.setEnabled(etat)
		self.pushButtonG58.setEnabled(etat)
		self.pushButtonG59.setEnabled(etat)
		self.pushButtonAnalyser.setEnabled(etat)
		self.action.setEnabled(etat)
		self.pushButtonOriginePiece.setEnabled(etat)
		self.pushButtonPriseOrigine.setEnabled(etat)
		self.pushButtonZ.setEnabled(etat)
		self.pushButton_Z.setEnabled(etat)
		self.pushButtonX.setEnabled(etat)
		self.pushButton_X.setEnabled(etat)
		self.pushButtonY.setEnabled(etat)
		self.pushButton_Y.setEnabled(etat)
		self.textEditCommande.setReadOnly(not etat)

	def etatPriseOrigine(self, etat):
		self.pushButtonConnecter.setEnabled(etat)
		self.pushButtonSearchPort.setEnabled(etat)
		self.pushButtonG54.setEnabled(etat)
		self.pushButtonG55.setEnabled(etat)
		self.pushButtonG56.setEnabled(etat)
		self.pushButtonG57.setEnabled(etat)
		self.pushButtonG58.setEnabled(etat)
		self.pushButtonG59.setEnabled(etat)
		self.pushButtonAnalyser.setEnabled(etat)
		self.action.setEnabled(etat)
		self.pushButtonOriginePiece.setEnabled(etat)
		self.pushButtonZ.setEnabled(etat)
		self.pushButton_Z.setEnabled(etat)
		self.pushButtonX.setEnabled(etat)
		self.pushButton_X.setEnabled(etat)
		self.pushButtonY.setEnabled(etat)
		self.pushButton_Y.setEnabled(etat)
		self.pushButtonPriseOrigine.setEnabled(etat)

	@pyqtSlot()
	def on_pushButtonPriseOrigine_clicked(self):
		if self.connecte:
			self.etatPriseOrigine(False)
			threadPriseOrigine=PriseOrigine(self.connexion.connexion)
			#timerThread.daemon=True
			threadPriseOrigine.start()
			while threadPriseOrigine.running:
				QCoreApplication.processEvents()
			
	
			if threadPriseOrigine.rxPriseOrigine[0].find("error:5")>-1:
				QMessageBox.warning(self, "erreur", "Le prise d'origine n'est pas active dans les paramètres")
			elif threadPriseOrigine.rxPriseOrigine[0].find("ok")>-1:
				QMessageBox.information(self, "action réussi", "La prise d'origine a réussi")#Si la prise d'origine réussie
			else:
				QMessageBox.warning(self, "prise d'origine échouée", "impossible de trouver les interrupteurs de fin de course" )

			for _ in range(len(threadPriseOrigine.rxPriseOrigine)):
				self.plainTextEditConsole.insertPlainText(threadPriseOrigine.rxPriseOrigine[_]	+"\n")
				self.plainTextEditConsole.moveCursor(QTextCursor.End)

			self.etatPriseOrigine(True)

		else:
			QMessageBox.information(self, "Aucune connexion", "Veillez d'abord vous connecter a la machine")




	
		




			

			



	
		















	def jogging(self, direction):
		if self.checkBoxCommandeManuelle.isChecked():
			self.etatJogging(False)
			self.progressBarJog.setVisible(True)
			feedRate=float(self.comboBoxFeedRate.currentText())
			distance=float(self.comboBoxDistance.currentText())
			commande=""


			if direction=="z":
				commande="$J=G91Z{}F{}\n".format(distance, feedRate)
				lcd_before=self.lcdNumberZM.value()
			
				#lcd_after=lcd_before+distance
				jog=True
				commande=commande.encode()
				print(commande)
				self.connexion.connexion.write("G4P0.01\n".encode())
				rx=self.connexion.connexion.readline().decode()
				self.connexion.connexion.write(commande)
				rx=self.connexion.connexion.readline().decode()
				print(rx)
				while jog:
					QCoreApplication.processEvents()
					self.connexion.connexion.write("?".encode())
					rx=self.connexion.connexion.readline().decode()
					print(rx)
				
					self.affichageCoordonnees(rx)
					lcd=self.lcdNumberZM.value()
					pourcentage=math.fabs(lcd-lcd_before)*100/distance
					self.progressBarJog.setValue(pourcentage)
					if self.labelEtat.text()=="Idle":
						jog=False


			elif direction=="-z":
				commande="$J=G91Z{}F{}\n".format(-1*distance, feedRate)
				lcd_before=self.lcdNumberZM.value()
				jog=True
				commande=commande.encode()
				print(commande)
				self.connexion.connexion.write("G4P0.01\n".encode())
				rx=self.connexion.connexion.readline().decode()
				self.connexion.connexion.write(commande)
				rx=self.connexion.connexion.readline().decode()
				print(rx)
				while jog:
					QCoreApplication.processEvents()
					self.connexion.connexion.write("?".encode())
					rx=self.connexion.connexion.readline().decode()
					print(rx)
					self.affichageCoordonnees(rx)
					lcd=self.lcdNumberZM.value()
					pourcentage=math.fabs(lcd-lcd_before)*100/distance
					self.progressBarJog.setValue(pourcentage)
					if self.labelEtat.text()=="Idle":
						jog=False

			elif direction=="y":
				commande="$J=G91Y{}F{}\n".format(distance, feedRate)
				lcd_before=self.lcdNumberYM.value()
			
				
				jog=True
				commande=commande.encode()
				print(commande)
				self.connexion.connexion.write("G4P0.01\n".encode())
				rx=self.connexion.connexion.readline().decode()
				self.connexion.connexion.write(commande)
				rx=self.connexion.connexion.readline().decode()
				print(rx)
				while jog:
					QCoreApplication.processEvents()
					self.connexion.connexion.write("?".encode())
					rx=self.connexion.connexion.readline().decode()
					print(rx)
					self.affichageCoordonnees(rx)
					lcd=self.lcdNumberYM.value()
					pourcentage=math.fabs(lcd-lcd_before)*100/distance
					self.progressBarJog.setValue(pourcentage)
					if self.labelEtat.text()=="Idle":
						jog=False
			elif direction=="-y":
				commande="$J=G91Y{}F{}\n".format(-1*distance, feedRate)
				lcd_before=self.lcdNumberYM.value()
		
				jog=True
				commande=commande.encode()
				print(commande)
				self.connexion.connexion.write("G4P0.01\n".encode())
				rx=self.connexion.connexion.readline().decode()
				self.connexion.connexion.write(commande)
				rx=self.connexion.connexion.readline().decode()
				print(rx)
				while jog:
					QCoreApplication.processEvents()
					self.connexion.connexion.write("?".encode())
					rx=self.connexion.connexion.readline().decode()
					print(rx)
					self.affichageCoordonnees(rx)
					lcd=self.lcdNumberYM.value()
					pourcentage=math.fabs(lcd-lcd_before)*100/distance
					self.progressBarJog.setValue(pourcentage)
					if self.labelEtat.text()=="Idle":
						jog=False
			elif direction=="x":
				commande="$J=G91X{}F{}\n".format(distance, feedRate)
				lcd_before=self.lcdNumberXM.value()
	
				jog=True
				commande=commande.encode()
				print(commande)
				self.connexion.connexion.write("G4P0.01\n".encode())
				rx=self.connexion.connexion.readline().decode()
				self.connexion.connexion.write(commande)
				rx=self.connexion.connexion.readline().decode()
				print(rx)
				while jog:
					QCoreApplication.processEvents()
					self.connexion.connexion.write("?".encode())
					rx=self.connexion.connexion.readline().decode()
					print(rx)
					self.affichageCoordonnees(rx)
					lcd=self.lcdNumberXM.value()
					pourcentage=math.fabs(lcd-lcd_before)*100/distance
					self.progressBarJog.setValue(pourcentage)
					if self.labelEtat.text()=="Idle":
						jog=False
			else:
				commande="$J=G91X{}F{}\n".format(-1*distance, feedRate)
				lcd_before=self.lcdNumberXM.value()
		
			
				jog=True
				commande=commande.encode()
				print(commande)
				self.connexion.connexion.write("G4P0.01\n".encode())
				rx=self.connexion.connexion.readline().decode()
				self.connexion.connexion.write(commande)
				rx=self.connexion.connexion.readline().decode()
				print(rx)
				while jog:
					QCoreApplication.processEvents()
					self.connexion.connexion.write("?".encode())
					rx=self.connexion.connexion.readline().decode()
					print(rx)
					self.affichageCoordonnees(rx)
					lcd=self.lcdNumberXM.value()
					pourcentage=math.fabs(lcd-lcd_before)*100/distance
					self.progressBarJog.setValue(pourcentage)
					if self.labelEtat.text()=="Idle":
						jog=False
			self.etatJogging(True)


# Lorsqu'on appuie sur le boutton
	@pyqtSlot()
	def on_pushButtonG54_pressed(self):
		if self.repereActif=="1":
			self.pushButtonG54.setIcon(QIcon("images/G54A.PNG"))
		else:
			self.pushButtonG54.setIcon(QIcon("images/G5A.PNG"))

	@pyqtSlot()
	def on_pushButtonG55_pressed(self):

		if self.repereActif=="2":
			self.pushButtonG55.setIcon(QIcon("images/G55AP.PNG"))
		else:
			self.pushButtonG55.setIcon(QIcon("images/G55P.PNG"))

	@pyqtSlot()
	def on_pushButtonG56_pressed(self):
		if self.repereActif=="3":
			self.pushButtonG56.setIcon(QIcon("images/G56AP.PNG"))
		else:
			self.pushButtonG56.setIcon(QIcon("images/G56P.PNG"))
	@pyqtSlot()
	def on_pushButtonG57_pressed(self):
		if self.repereActif=="4":
			self.pushButtonG57.setIcon(QIcon("images/G57AP.PNG"))
		else:
			self.pushButtonG57.setIcon(QIcon("images/G57P.PNG"))

	@pyqtSlot()
	def on_pushButtonG58_pressed(self):
		if self.repereActif=="5":
			self.pushButtonG58.setIcon(QIcon("images/G58AP.PNG"))
		else:
			self.pushButtonG58.setIcon(QIcon("images/G58P.PNG"))

	@pyqtSlot()
	def on_pushButtonG59_pressed(self):
		if self.repereActif=="6":
			self.pushButtonG59.setIcon(QIcon("images/G59AP.PNG"))
		else:
			self.pushButtonG59.setIcon(QIcon("images/G59P.PNG"))




	@pyqtSlot()
	def on_pushButtonG54_released(self):
		if self.repereActif=="1":
			self.pushButtonG54.setIcon(QIcon("images/G54A.PNG"))
		else:
			self.pushButtonG54.setIcon(QIcon("images/G54.PNG"))
			

	@pyqtSlot()
	def on_pushButtonG55_released(self):

		if self.repereActif=="2":
			self.pushButtonG55.setIcon(QIcon("images/G55A.PNG"))
		else:
			self.pushButtonG55.setIcon(QIcon("images/G55E.PNG"))
			
	@pyqtSlot()
	def on_pushButtonG56_released(self):
		if self.repereActif=="3":
			self.pushButtonG56.setIcon(QIcon("images/G56A.PNG"))
		else:
			self.pushButtonG56.setIcon(QIcon("images/G56.PNG"))
	@pyqtSlot()
	def on_pushButtonG57_released(self):
		if self.repereActif=="4":
			self.pushButtonG57.setIcon(QIcon("images/G57A.PNG"))
		else:
			self.pushButtonG57.setIcon(QIcon("images/G57.PNG"))


	@pyqtSlot()
	def on_pushButtonG58_released(self):
		if self.repereActif=="5":
			self.pushButtonG58.setIcon(QIcon("images/G58A.PNG"))
		else:
			self.pushButtonG58.setIcon(QIcon("images/G58.PNG"))
	@pyqtSlot()
	def on_pushButtonG59_released(self):
		if self.repereActif=="6":
			self.pushButtonG59.setIcon(QIcon("images/G59A.PNG"))
		else:
			self.pushButtonG59.setIcon(QIcon("images/G59.PNG"))



	@pyqtSlot()
	def on_pushButtonG54_clicked(self):
		if self.connecte:
			self.wco="1"
			self.messageBoxG=MessageBoxG(self)
			self.messageBoxG.setWindowModality(Qt.ApplicationModal)# Definir la modalité de la deuxieme fenêtre
			self.messageBoxG.show()
		else:
			QMessageBox.information(self, "aucune connexion", "veillez  vous connecter") 


		

	@pyqtSlot()
	def on_pushButtonG55_clicked(self):
		if self.connecte:
			self.wco="2"
			self.messageBoxG=MessageBoxG(self)
			self.messageBoxG.setWindowModality(Qt.ApplicationModal)# Definir la modalité de la deuxieme fenêtre
			self.messageBoxG.show()
		else:
			QMessageBox.information(self, "aucune connexion", "veillez  vous connecter") 		
	@pyqtSlot()
	def on_pushButtonG56_clicked(self):
		if self.connecte:
			self.wco="3"
			self.messageBoxG=MessageBoxG(self)
			self.messageBoxG.setWindowModality(Qt.ApplicationModal)# Definir la modalité de la deuxieme fenêtre
			self.messageBoxG.show()
		else:
			QMessageBox.information(self, "aucune connexion", "veillez  vous connecter") 
		
	@pyqtSlot()
	def on_pushButtonG57_clicked(self):
		if self.connecte:
			self.wco="4"
			self.messageBoxG=MessageBoxG(self)
			self.messageBoxG.setWindowModality(Qt.ApplicationModal)# Definir la modalité de la deuxieme fenêtre
			self.messageBoxG.show()
		else:
			QMessageBox.information(self, "aucune connexion", "veillez  vous connecter") 

	@pyqtSlot()
	def on_pushButtonG58_clicked(self):
		if self.connecte:
			self.wco="5"
			self.messageBoxG=MessageBoxG(self)
			self.messageBoxG.setWindowModality(Qt.ApplicationModal)# Definir la modalité de la deuxieme fenêtre
			self.messageBoxG.show()
		else:
			QMessageBox.information(self, "aucune connexion", "veillez  vous connecter") 

		
	@pyqtSlot()
	def on_pushButtonG59_clicked(self):
		if self.connecte:
			self.wco="6"
			self.messageBoxG=MessageBoxG(self)
			self.messageBoxG.setWindowModality(Qt.ApplicationModal)# Definir la modalité de la deuxieme fenêtre
			self.messageBoxG.show()
		else:
			QMessageBox.information(self, "aucune connexion", "veillez  vous connecter") 


	@pyqtSlot()
	def on_pushButtonG55_hover(self):
		print("TMLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLllll")






	def etatStreamer(self, etat):

		self.pushButtonAnalyser.setEnabled(etat)
		self.progressBar.setVisible(etat)
		self.pushButtonBreak.setVisible(not etat)
			
		self.pushButtonArreter.setVisible(not etat)
		self.pushButtonConnecter.setEnabled(etat)
		self.pushButtonG54.setEnabled(etat)
		self.pushButtonG55.setEnabled(etat)
		self.pushButtonG56.setEnabled(etat)
		self.pushButtonG57.setEnabled(etat)
		self.pushButtonG58.setEnabled(etat)
		self.pushButtonG59.setEnabled(etat)
		self.checkBoxCommandeManuelle.setChecked(etat)
		self.checkBoxCommandeManuelle.setEnabled(etat)
		self.pushButtonImportFichier.setEnabled(etat)
		self.pushButtonSearchPort.setEnabled(etat)
		self.action.setEnabled(etat)
		self.pushButtonPriseOrigine.setEnabled(etat)
		self.pushButtonGraverDessiner.setEnabled(etat)
		MainWindowSender.ARRETER=False
		MainWindowSender.STREAMER=True
		MainWindowSender.ENACTIVITE=not etat
		MainWindowSender.EN_ARRET=False
		self.textEditCommande.setReadOnly(not etat)
		

		if etat==True:
			
			self.connexion.connexion.write("?\n".encode())
			reception=self.connexion.connexion.read_until().decode()
			print(reception, "reception  ----------------")
			self.affichageCoordonnees(reception)
			print("TML-------------------------------------")
			reception=self.connexion.connexion.read_until().decode().strip()

		
			print(reception, "reception  ----------------")
	
			self.labelTempsRestant.setText("0 sec")

			
		#self.connexion.connexion.write("G4P0.1\n".encode())
		#self.connexion.connexion.read(self.connexion.connexion.inWaiting())
		
		
		
		###########################################################################""
	






		





	def streamer(self):
		self.etatStreamer(False)
		compteur_gcode_envoye=0
		tab_lignes=[]
		tab_gcodes=[]
		tab_temps=[]
		rang_ligne=0
		#self.pushButtonBreak.setVisible(True)
		#self.pushButtonGraverDessiner.setEnabled(False)
		#self.pushButtonAnalyser.setEnabled(False)
		self.labelNombreDeLignes.setText(str(self.lignes))
		self.progressBar.setVisible(True)
		with open(self.fichier, "r") as file:
			
			for ligne in file:
				rang_ligne+=1
				gcode=re.sub('\s|\(.*?\)','',ligne).upper()
				tab_lignes.append(len(gcode)+1)
				tab_gcodes.append(gcode)
				tab_temps.append(time.time())
				tx=""
				#QCoreApplication.processEvents()
				while enPause:
					time.sleep(0.05)
					#QCoreApplication.processEvents()

				QCoreApplication.processEvents()

				while sum(tab_lignes)>=TAILLE_BUFFER_RX-1  | self.connexion.connexion.inWaiting():
					tx=self.connexion.connexion.readline().strip().decode()
					QCoreApplication.processEvents()
					

					if tx.find("error")<0 & tx.find("ok")<0:
						self.plainTextEditConsole.insertPlainText(tx)
					else:
						compteur_gcode_envoye+=1
						self.plainTextEditConsole.insertPlainText(str(compteur_gcode_envoye)+"   "+ tab_gcodes[0]+"  "+tx+"\n")
						temps=time.time()-tab_temps[0]
						del(tab_temps[0])
						del(tab_gcodes[0])
						del(tab_lignes[0])
					self.plainTextEditConsole.moveCursor(QTextCursor.End)
					self.plainTextEditConsole.ensureCursorVisible()
					print(temps)
					self.progressBar.setValue(compteur_gcode_envoye*100/self.lignes)
					self.labelLignesRestantes.setText(str(self.lignes-compteur_gcode_envoye))
					self.labelTempsTotal.setText(self.conversionTemps(int(temps*self.lignes)))
					self.labelVitesse.setText(str((math.ceil(1/temps))))
					QCoreApplication.processEvents()
				writen=gcode+"\n"
				self.connexion.connexion.write(writen.encode())
				QCoreApplication.processEvents()
			

			while rang_ligne>compteur_gcode_envoye:
				tx=self.connexion.connexion.readline().strip().decode()
				if tx.find("error")<0 & tx.find("ok")<0:
					self.plainTextEditConsole.insertPlainText(tx)
				else:
					compteur_gcode_envoye+=1
					self.plainTextssEditConsole.insertPlainText(str(compteur_gcode_envoye)+"  "+tx+"\n")
					self.plainTextEditConsole.insertPlainText(str(compteur_gcode_envoye)+"   "+ tab_gcodes[0]+"  "+tx+"\n")
					temps=time.time()-tab_temps[0]
					del(tab_temps[0])
					del(tab_gcodes[0])
					del(tab_lignes[0])
				self.plainTextEditConsole.moveCursor(QTextCursor.End)
				self.plainTextEditConsole.ensureCursorVisible()
				print(temps)
				self.progressBar.setValue(compteur_gcode_envoye*100/self.lignes)
				self.labelLignesRestantes.setText(str(self.lignes-compteur_gcode_envoye))
				self.labelTempsTotal.setText(self.conversionTemps(int(temps*self.lignes)))
				self.labelVitesse.setText(int(1/temps))
				QCoreApplication.processEvents()

		self.etatStreamer(True)








					


				

				

				







	def conversionTemps(self, temps):
		secondes=temps
		if secondes<60:
			return self.tronquerDec(secondes)+" sec"
		if (secondes>=60 and secondes<3600):
			minutes=secondes//60
			secondes=secondes-minutes*60
			return str(minutes)+" min: "+self.tronquerDec(secondes)+" sec"
		if secondes>=3600:
			heures=secondes//3600
			secondes=secondes-heures*3600
			if secondes<60:
				return str(heures)+" h: "+self.tronquerDec(secondes)+" sec"
			if secondes>=60 and secondes<3600:
				minutes=secondes//60
				secondes=secondes-minutes*60
				return str(heures)+" h: "+str(minutes)+" min: "+self.tronquerDec(secondes)+" s"

	def tronquerDec(self, n):
		n=str(n)
		index=n.find(".")
		if index>=0:
			return str(n[:index+3])
		return str(n)





	def rapports(self):
		l=None
		while MainWindowSender.ENACTIVITE: 
			if  not MainWindowSender.ENPAUSE:
				temps1=time.time()
				l=self.connexion.connexion.write(self.commande_rapport)
				print(time.time()-temps1, "temps solution-------------")
				time.sleep(1)

				

	

				#time.sleep(INTERVAL_DE_RAPPORT)

#############################################################################################		


		
			#tx=self.connexion.connexion.readline().decode()
			#if tx.find("<")>0:
			#	pass
	
		
			

	




	def closeEvent(self, event):
		"""
		if not self.fermable:
			QMessageBox.warning(self, "opération en cours", "veillez attendre la fin de l'opération ou annulez l'opération ")
			event.ignore()
			return
			"""
		if self.connecte:
			reponse=QMessageBox.question(self, "confirmation", "Voulez vous vraimant couper la connexion ??", QMessageBox.No, QMessageBox.Yes)
			if reponse==QMessageBox.Yes:
				self.connexion.connexion.close()
				event.accept()
			else:
				event.ignore()



class ThreadConnexion(QRunnable):
	def __init__(self, fichier, connexion, lignes):                                       
		super(ThreadConnexion, self).__init__()
		self.fichier=fichier
		self.connexion=connexion
		self.lignes=lignes
		self.time=0
		self.commande_rapport='?'.encode()
		#self.connexion.flushInput()
		self.connexion.write_timeout=0
		self.nombredeOk=0
		self.effect=0
		

	def streamer(self):
		self.connexion.flushInput()
		compteur_gcode_envoye=0.0000000000000000000000001
		tab_lignes=[]
		tab_gcodes=[]
		tab_temps=[]
		temps_debut=time.time()
		rang_ligne=0

		with open(self.fichier, "r") as file:
			
			for ligne in file:
				"""
				

				if time.time()-self.time>=0.2:
					self.rapports()
					self.time=time.time()
					"""
					

				

			
				rang_ligne+=1
				print(rang_ligne)
				gcode=re.sub('\s|\(.*?\)','',ligne).upper()
				tab_lignes.append(len(gcode)+1)
				tab_gcodes.append(gcode)
				tab_temps.append(time.time())
			
				tx=""
				#print("TML")
				#self.connexion.write("?\n")
				#RAPPORTS.append(self.connexion.readline().strip().decode())
				#QCoreApplication.processEvents()

				while MainWindowSender.ENPAUSE:
					time.sleep(0.05)
					QCoreApplication.processEvents()
					print("TML")
					if MainWindowSender.ARRETER:
						MainWindowSender.ENPAUSE=False
						MainWindowSender.EN_ARRET=True
						MainWindowSender.ENACTIVITE=False
						print("###########################################")

					#print(MainWindowSender.ARRETER)
			
			
				
				if  MainWindowSender.ARRETER:
					print("En arrêt première ------------------------------------ ")
					print("ARRETER", MainWindowSender.ARRETER)
					#MainWindowSender.STREAMER=False
					
					MainWindowSender.ENACTIVITE=False
					MainWindowSender.EN_ARRET=True
				
					
					
				

					while sum(tab_lignes)>=TAILLE_BUFFER_RX-1 | self.connexion.inWaiting():
						if MainWindowSender.ARRETER:
							MainWindowSender.EN_ARRET=True
							"""
							
						if time.time()-self.time>=0.2:
							self.rapports()
							self.time=time.time()
							"""
							

						
						tx=self.connexion.readline().strip().decode()
						if tx[:3].find("ok")>=0:
							compteur_gcode_envoye+=1
							plainTextEditConsole.append(str(compteur_gcode_envoye)+"   "+ tab_gcodes[0]+"  "+tx+"\n")
							temps=time.time()-tab_temps[0]
							#tab_temps.append(time.time())
							del(tab_temps[0])
							del(tab_gcodes[0])
							del(tab_lignes[0])
						elif tx.find("error")>=0:
							compteur_gcode_envoye+=1
							plainTextEditConsole.append(str(compteur_gcode_envoye)+"   "+ tab_gcodes[0]+"  "+tx+"\n")
							temps=time.time()-tab_temps[0]
							del(tab_temps[0])
							del(tab_gcodes[0])
							del(tab_lignes[0])
			
						
						else: 
							plainTextEditCommande.append(tx+  "\n")
							temps=time.time()-tab_temps[0]
						#self.plainTextEditConsole.moveCursor(QTextCursor.End)
						#self.plainTextEditConsole.ensureCursorVisible()
						print(temps)
						progressBar.append(compteur_gcode_envoye*100/self.lignes)
						labelLignesRestantes.append(str(self.lignes-compteur_gcode_envoye))
						labelTempsRestant.append((( time.time()-temps_debut)/compteur_gcode_envoye)*(self.lignes-compteur_gcode_envoye))
						labelVitesse.append(str((math.ceil(1/temps))))
						#QCoreApplication.processEvents()
					WRITING=True
					writen=gcode+"\n"
					WRITING=False
					#self.connexion.timeout=0


					self.write(writen.encode())
					#self.connexion.timeout=None
					#self.connexion.write("?\n".encode())
					#rapports=self.connexion.readline().strip().decode()
					#print(rapports)
					#QCoreApplication.processEvents()
					print(rang_ligne,"rang----------------------------------------------")
					print(compteur_gcode_envoye,"------------------------------")

					break

		


					



				while sum(tab_lignes)>=TAILLE_BUFFER_RX-1 | self.connexion.inWaiting():
					if MainWindowSender.ARRETER:
						MainWindowSender.EN_ARRET=True
						MainWindowSender.ENACTIVITE=False
					while MainWindowSender.ENPAUSE:
					
						time.sleep(0.05)
						QCoreApplication.processEvents()


						print("TML:::::::::::::::::::::::::::::::::::::")
						if MainWindowSender.ARRETER:
							MainWindowSender.ENPAUSE=False
							MainWindowSender.EN_ARRET=True
							MainWindowSender.ENACTIVITE=False

					"""
							

					if time.time()-self.time>=0.2:
						self.rapports()
						self.time=time.time()
					"""
						


			

					"""if  MainWindowSender.ARRETER:
						print("ARRETER", MainWindowSender.ARRETER)
						MainWindowSender.STREAMER=False
						MainWindowSender.ENACTIVITE=False
						#return self.tml()
						"""




					tx=self.connexion.readline().strip().decode()

					

					
					if tx[:3].find("ok")>=0:
						compteur_gcode_envoye+=1
						plainTextEditConsole.append(str(compteur_gcode_envoye)+"   "+ tab_gcodes[0]+"  "+tx+"\n")
						temps=time.time()-tab_temps[0]
						del(tab_temps[0])
						del(tab_gcodes[0])
						del(tab_lignes[0])
						self.nombredeOk+=1
				
					elif tx.find("error")>=0:
						compteur_gcode_envoye+=1
						plainTextEditConsole.append(str(compteur_gcode_envoye)+"   "+ tab_gcodes[0]+"  "+tx+"\n")
						temps=time.time()-tab_temps[0]
						del(tab_temps[0])
						del(tab_gcodes[0])
						del(tab_lignes[0])
			
					else: 
						plainTextEditCommande.append(tx+  "\n")
						temps=time.time()-tab_temps[0]
				
						
					#self.plainTextEditConsole.moveCursor(QTextCursor.End)
					#self.plainTextEditConsole.ensureCursorVisible()
					print(temps)
					progressBar.append(compteur_gcode_envoye*100/self.lignes)
					labelLignesRestantes.append(str(self.lignes-compteur_gcode_envoye))
					labelTempsRestant.append((( time.time()-temps_debut)/compteur_gcode_envoye)*(self.lignes-compteur_gcode_envoye))

					#labelVitesse.append(str((math.ceil(1/temps))))
					#QCoreApplication.processEvents()
				WRITING=True
				writen=gcode+"\n"
				WRITING=False
				#self.connexion.timeout=0
				print(compteur_gcode_envoye, "compteur_gcode_envoye-----------------")



				self.write(writen.encode())
				print("ligne", rang_ligne," envoyée--------------------")
				
	

			
				
				#self.connexion.timeout=None
				#self.connexion.write("?\n".encode())
				#rapports=self.connexion.readline().strip().decode()
				#print(rapports)
				#QCoreApplication.processEvents()

			print(compteur_gcode_envoye, "compteur_gcode_envoyé-----fin------------")
			print(rang_ligne,"rang_ligne ---------------------------fin-------------")

			while rang_ligne>compteur_gcode_envoye:
				MainWindowSender.ENACTIVITE=False
				if MainWindowSender.ARRETER:
					print("En arrêt deuxieme--------------------------------------------")
					MainWindowSender.ENACTIVITE=False
					MainWindowSender.EN_ARRET=True
				while MainWindowSender.ENPAUSE:
						time.sleep(0.05)
						QCoreApplication.processEvents()
						print("TML:::::::::::::::::::::::::::::::::::::")
						if MainWindowSender.ARRETER:
							MainWindowSender.ENPAUSE=False
							MainWindowSender.EN_ARRET=True
							MainWindowSender.ENACTIVITE=False

		
				print(compteur_gcode_envoye, "compteur_gcode_envoyé-----------------")
				print(rang_ligne,"rang_ligne ----------------------------------------") 


				print("C'est toi qui bloque??")
				print(MainWindowSender.ENACTIVITE)
				
				tx=self.connexion.readline().strip().decode()
				print("oui")
				if tx[:3].find("ok")>=0:
					compteur_gcode_envoye+=1
					plainTextEditConsole.append(str(compteur_gcode_envoye)+"   "+ tab_gcodes[0]+"  "+tx+"\n")
					temps=time.time()-tab_temps[0]
					del(tab_temps[0])
					del(tab_gcodes[0])
					del(tab_lignes[0])
					self.nombredeOk+=1
				elif tx.find("error")>=0:
					compteur_gcode_envoye+=1
					plainTextEditConsole.append(str(compteur_gcode_envoye)+"   "+ tab_gcodes[0]+"  "+tx+"\n")
					temps=time.time()-tab_temps[0]
					del(tab_temps[0])
					del(tab_gcodes[0])
					del(tab_lignes[0])
				else: 
					print("rapport encore ??????????????????????,")
					plainTextEditCommande.append(tx+  "\n")
					temps=time.time()-tab_temps[0]


				
				

				#plainTextEditConsole.moveCursor(QTextCursor.End)
				#self.plainTextEditConsole.ensureCursorVisible()s
				#print(temps)
				print("nombre de ok ", self.nombredeOk, "okokokokokookokokokokokokokokokokoks")
				progressBar.append(compteur_gcode_envoye*100/self.lignes)
				labelLignesRestantes.append(str(self.lignes-compteur_gcode_envoye))
				#labelTempsTotal.append(self.conversionTemps(int(temps*self.lignes)))
				labelVitesse.append(int(1/temps))
				QCoreApplication.processEvents()
				#time.sleep(0.3)
			
			print("restant--------------------------------------------------")
			self.connexion.write("G4P0.01\n".encode())
			l=self.connexion.readline().decode()
			print("G4PO.O1, --------",l)
			#print(self.connexion.readline().decode())
			MainWindowSender.STREAMER=False



	def write(self, data):

		l=None
		#MainWindowSender.ecrire=False
		#time.sleep(0.1)
	
		l=self.connexion.write(data)
		self.effect+=1
	

		#time.sleep(0.05)

		
		
		

		"""
		try:
			l=self.connexion.write(data)
		except:
			print("=================================================================")
			return self.write(data)
			"""
		




	def tml(self):
		print("interrompue par TML")

	def rapports(self):
		#self.connexion.flusInput()
		l=None
		
	
		
		

		while MainWindowSender.ENACTIVITE: 
			if  not MainWindowSender.ENPAUSE:
				temps1=time.time()
				l=self.connexion.write(self.commande_rapport)
				print(time.time()-temps1, "temps solution-------------")
				time.sleep(0.2)
		

				
			
			




	@pyqtSlot()
	def run(self):
		
	
		thread=Thread(target=self.rapports)
		thread.daemon=True
		thread.start()
		
		

		self.streamer()  
		#print("TMLL")


def fonctionThreadRapport(connexion):
	while MainWindowSender.STREAMER:
		print(RAPPORTS)
		
		connexion.write("?".encode())


		time.sleep(INTERVAL_DE_RAPPORT)
		tx=connexion.readline().decode()
		if tx[:3].find("<")>0:
			#RAPPORTS.append(tx)
			pass




	
	


		
		
		




    









