"""Dialog allowing the user to inspect and tweak GRBL configuration values."""

import csv

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QListWidget, QMainWindow, QMessageBox

from ..forms.configurator_ui import Ui_Form

class Configurateur(QMainWindow, Ui_Form):
	def __init__(self, connexion, output, labelUnite_):
		super(Configurateur, self).__init__()
		self.setupUi(self)
		self.move(200, 0)
		self.setWindowTitle("Configurations")
		self.settings=[]
		self.labelUnite_=labelUnite_

		with open("parametre_codes_en_Fr.csv", "r") as file:
			fichier_csv=csv.reader(file, delimiter=",")
			i=0
			for row in fichier_csv:
		

				self.listWidget.insertItem(i, row[1])
				self.settings.append(row)
				i+=1
		self.listWidget.setCurrentRow(0)

		
		self.listWidget.currentRowChanged.connect(self.test)
		self.modifications={}
		
		self.index=0
		self.masque=["00000000", "00000001", "00000010", "00000011", "00000100","00000101","00000110","00000111"]

		self.connexion=connexion
		self.output=output
		self.connexion.write("$$\n".encode())
		rx=""
		condition=True
		while True:
			rx=self.connexion.readline().decode().strip()
			if rx=="ok":
				condition=False
				break
			debut_numero=1
			fin_numero=rx.find("=")
			numero=rx[debut_numero:fin_numero]
			print(rx)
			print(numero)
			numero=int(numero)
			valeur=rx[fin_numero+1:]
			self.modifications[numero]=valeur
		if self.modifications[13]=="0":
			self.labelUnite_.setText("millimetre(mm)")

		else:
			self.labelUnite_.setText("pouce")


		self.test()
			
			



	

	def test(self):
		#item=self.listWidget.currentItem()
		self.index=self.listWidget.currentRow()

		self.plainTextEdit.setPlainText(self.settings[self.index][3])
		if self.index==0:
			self.comboBox.clear()
			self.comboBox.setEditable(True)
		
			for _ in [ "3", "5", "10","15", "20","25", "30"]:
				self.comboBox.addItem(_)
				self.comboBox.setCurrentText(self.modifications[0])
			self.labelUnite.setText("microsecondes(µs)")
		if self.index==1:
			
			self.comboBox.clear()

			self.comboBox.setEditable(True)
			self.labelUnite.setText("millisecondes(ms)")
			self.comboBox.setCurrentText(self.modifications[1])
		if self.index==2:
			
			self.labelUnite.setText("masque binaire")
			self.comboBox.clear()
			self.comboBox.setEditable(False)

			for _ in self.masque:
				self.comboBox.addItem(_)
			self.comboBox.setCurrentIndex(self.conversionBinaireDecimal(self.modifications[2]))
		if self.index==3:
			
			self.comboBox.clear()
			self.labelUnite.setText("masque binaire")
			self.comboBox.setEditable(False)
			for _ in self.masque:
				self.comboBox.addItem(_)
			self.comboBox.setCurrentIndex(self.conversionBinaireDecimal(self.modifications[3]))


		if self.index==4:

			self.comboBox.clear()
			self.labelUnite.setText("booléen")
			self.comboBox.setEditable(False)
			self.comboBox.addItem("0")
			self.comboBox.addItem("1")
			self.comboBox.setCurrentText(self.modifications[4])
		if self.index==5:
			self.comboBox.clear()
			self.labelUnite.setText("booléen")
			self.comboBox.setEditable(False)
			self.comboBox.addItem("0")
			self.comboBox.addItem("1")
			self.comboBox.setCurrentText(self.modifications[5])
		if self.index==6:
			self.comboBox.clear()
			self.labelUnite.setText("booléen")
			self.comboBox.setEditable(False)
			self.comboBox.addItem("0")
			self.comboBox.addItem("1")
			self.comboBox.setCurrentText(self.modifications[6])
		if self.index==7:
			self.comboBox.clear()
			self.labelUnite.setText("millimetre(mm)")
			self.comboBox.setEditable(True)
			self.comboBox.setCurrentText(self.modifications[11])
		if self.index==8:
			self.comboBox.clear()
			self.labelUnite.setText("millimetre(mm)")
			self.comboBox.setEditable(True)
			self.comboBox.setCurrentText(self.modifications[12])
		if self.index==9:
			self.comboBox.clear()
			self.labelUnite.setText("booléen")
			self.comboBox.setEditable(False)
			self.comboBox.addItem("0")
			self.comboBox.addItem("1")
			self.comboBox.setCurrentText(self.modifications[13])
		if self.index==10:
			self.comboBox.clear()
			self.labelUnite.setText("booléen")
			self.comboBox.setEditable(False)
			self.comboBox.addItem("0")
			self.comboBox.addItem("1")
			self.comboBox.setCurrentText(self.modifications[20])
		if self.index==11:
			self.comboBox.clear()
			self.labelUnite.setText("booléen")
			self.comboBox.setEditable(False)
			self.comboBox.addItem("0")
			self.comboBox.addItem("1")
			self.comboBox.setCurrentText(self.modifications[21])
		if self.index==12:
			self.comboBox.clear()
			self.labelUnite.setText("booléen")
			self.comboBox.setEditable(False)
			self.comboBox.addItem("0")
			self.comboBox.addItem("1")
			self.comboBox.setCurrentText(self.modifications[22])
		if self.index==13:
			self.labelUnite.setText("masque binaire")
			self.comboBox.clear()
			self.comboBox.setEditable(False)
			for _ in self.masque:
				self.comboBox.addItem(_)
			self.comboBox.setCurrentIndex(self.conversionBinaireDecimal(self.modifications[23]))
		if self.index==14:
			self.comboBox.clear()
			self.labelUnite.setText("mm/min")
			self.comboBox.setEditable(True)
			self.comboBox.setCurrentText(self.modifications[24])
		if self.index==15:
			self.comboBox.clear()
			self.labelUnite.setText("millisecondes")
			self.comboBox.setEditable(True)
			self.comboBox.setCurrentText(self.modifications[25])
		if self.index==16:
			self.comboBox.clear()
			self.comboBox.setEditable(True)
			self.labelUnite.setText("milliseconde(ms)")
			self.comboBox.setCurrentText(self.modifications[26])
		if self.index==17:
			self.comboBox.clear()
			self.comboBox.setEditable(True)
			self.labelUnite.setText("millimetre(mm)")
			self.comboBox.setCurrentText(self.modifications[27])

		if self.index==18:
			self.comboBox.clear()
			self.comboBox.setEditable(True)
			self.labelUnite.setText("tr/min")
			self.comboBox.setCurrentText(self.modifications[30])
		if self.index==19:
			self.comboBox.clear()
			self.comboBox.setEditable(True)
			self.labelUnite.setText("tr/min")
			self.comboBox.setCurrentText(self.modifications[31])
		if self.index==20:
			self.comboBox.clear()
			self.labelUnite.setText("booléan")
			self.comboBox.setEditable(False)
			self.comboBox.addItem("0")
			self.comboBox.addItem("1")
			self.comboBox.setCurrentText(self.modifications[32])
		if self.index==21:
			self.comboBox.clear()
			self.comboBox.setEditable(True)
			self.labelUnite.setText("pas/mm")
			self.comboBox.setCurrentText(self.modifications[100])
		if self.index==22:
			self.comboBox.clear()
			self.comboBox.setEditable(True)
			self.labelUnite.setText("pas/mm")
			self.comboBox.setCurrentText(self.modifications[101])
		if self.index==23:
			self.comboBox.clear()
			self.comboBox.setEditable(True)
			self.labelUnite.setText("pas/mm")
			self.comboBox.setCurrentText(self.modifications[102])
		if self.index==24:
			self.comboBox.clear()
			self.comboBox.setEditable(True)
			self.labelUnite.setText("mm/min")
			self.comboBox.setCurrentText(self.modifications[110])
		if self.index==25:
			self.comboBox.clear()
			self.comboBox.setEditable(True)
			self.labelUnite.setText("mm/min")
			self.comboBox.setCurrentText(self.modifications[111])
		if self.index==26:
			self.comboBox.clear()
			self.comboBox.setEditable(True)
			self.labelUnite.setText("mm/min")
			self.comboBox.setCurrentText(self.modifications[112])
		if self.index==27:
			self.comboBox.clear()
			self.comboBox.setEditable(True)
			self.labelUnite.setText("mm/s^2")
			self.comboBox.setCurrentText(self.modifications[120])
		if self.index==28:
			self.comboBox.clear()
			self.comboBox.setEditable(True)
			self.labelUnite.setText("mm/s^2")
			self.comboBox.setCurrentText(self.modifications[121])
		if self.index==29:
			self.comboBox.clear()
			self.comboBox.setEditable(True)
			self.labelUnite.setText("mm/s^2")
			self.comboBox.setCurrentText(self.modifications[122])
		if self.index==30:
			self.comboBox.clear()
			self.comboBox.setEditable(True)
			self.labelUnite.setText("mm")
			self.comboBox.setCurrentText(self.modifications[130])
		if self.index==31:
			self.comboBox.clear()
			self.comboBox.setEditable(True)
			self.labelUnite.setText("mm")
			self.comboBox.setCurrentText(self.modifications[131])

		if self.index==32:
			self.comboBox.clear()
			self.comboBox.setEditable(True)
			self.labelUnite.setText("mm")
			self.comboBox.setCurrentText(self.modifications[132])
		

		
		
		
		
		
		
		
		
	
		
	

	

	
		
	
		











		

	@pyqtSlot()
	def on_pushButtonOk_clicked(self):
		valeur=self.comboBox.currentText()
		try:
			float(valeur)
		except:
			QMessageBox.information(self, "Erreur", "Entrez un nombre")
		else:
			if self.index==0:
				if float(valeur)<3:
					QMessageBox.information(self, "Erreur", "La valeur minimale est de 3 µs")
					
				else:
					self.modifications[self.index]=valeur
			if self.index==1:
				if (float(valeur)<0 or float(valeur)>255):
					QMessageBox.information(self, "erreur", "la valeur doit compris entre 0 et 255")
				else:
					self.modifications[self.index]=valeur
			if self.index==2:
				self.modifications[self.index]=valeur
			if self.index==3:
				self.modifications[self.index]=valeur

			if self.index==4:
				self.modifications[self.index]=valeur
			if self.index==5:
				self.modifications[self.index]=valeur

			if self.index==6:
				self.modifications[self.index]=valeur
			if self.index==7:
				if float(valeur)<0:
					QMessageBox.information(self, "erreur","Entrez un nombre positif")
				else:
					self.modifications[11]=valeur
			if self.index==8:
				if float(valeur)<0:
					QMessageBox.information(self, "erreur", "Entrez un nombre positif")
				else:
					self.modifications[12]=valeur
			if self.index==9:
				self.modifications[13]=valeur
			if self.index==10:
				self.modifications[20]=valeur
			if self.index==11:
				self.modifications[21]=valeur
			if self.index==12:
				self.modifications[22]=valeur
			if self.index==13:
				self.modifications[23]=valeur
			if self.index==14:
				if float(valeur)<0:
					QMessageBox.information(self,"erreur", "Entrez un nombre positif")
				else:
					self.modifications[24]=valeur
			if self.index==15:
				if float(valeur)<0:
					QMessageBox.information(self,"erreur", "Entrez un nombre positif")
				else:
					self.modifications[25]=valeur
			if self.index==16:
				if float(valeur)<0:
					QMessageBox.information(self,"erreur", "Entrez un nombre positif")
				else:
					self.modifications[26]=valeur
			if self.index==17:
				if float(valeur)<0:
					QMessageBox.information(self,"erreur", "Entrez un nombre positif")
				else:
					self.modifications[27]=valeur
			if self.index==18:
				if float(valeur)<0:
					QMessageBox.information(self, "erreur", "Entrez un nombre positif")
				else:
					self.modifications[30]=valeur
			if self.index==19:
				if float(valeur)<0:
					QMessageBox.information(self, "erreur", "Entrez un nombre positif")
				else:
					self.modifications[31]=valeur
			if self.index==20:
				self.modifications[32]=valeur
			if self.index==21:
				if float(valeur)<0:
					QMessageBox.information(self, "erreur", "Entrez un nombre positif")
				else:
					self.modifications[100]=valeur

			if self.index==22:
				if float(valeur)<0:
					QMessageBox.information(self, "erreur", "Entrez un nombre positif")
				else:
					self.modifications[101]=valeur
			if self.index==23:
				if float(valeur)<0:
					QMessageBox.information(self, "erreur", "Entrez un nombre positif")
				else:
					self.modifications[102]=valeur

			if self.index==24:
				if float(valeur)<0:
					QMessageBox.information(self, "erreur", "Entrez un nombre positif")
				else:
					self.modifications[110]=valeur

			if self.index==25:
				if float(valeur)<0:
					QMessageBox.information(self, "erreur", "Entrez un nombre positif")
				else:
					self.modifications[111]=valeur
			if self.index==26:
				if float(valeur)<0:
					QMessageBox.information(self, "erreur", "Entrez un nombre positif")
				else:
					self.modifications[112]=valeur
			if self.index==27:
				if float(valeur)<0:
					QMessageBox.information(self, "erreur", "Entrez un nombre positif")
				else:
					self.modifications[120]=valeur
			if self.index==28:
				if float(valeur)<0:
					QMessageBox.information(self, "erreur", "Entrez un nombre positif")
				else:
					self.modifications[121]=valeur

			if self.index==29:
				if float(valeur)<0:
					QMessageBox.information(self, "erreur", "Entrez un nombre positif")
				else:
					self.modifications[122]=valeur
			if self.index==30:
				if float(valeur)<0:
					QMessageBox.information(self, "erreur", "Entrez un nombre positif")
				else:
					self.modifications[130]=valeur
			if self.index==31:
				if float(valeur)<0:
					QMessageBox.information(self, "erreur", "Entrez un nombre positif")
				else:
					self.modifications[131]=valeur
			if self.index==32:
				if float(valeur)<0:
					QMessageBox.information(self, "erreur", "Entrez un nombre positif")
				else:
					self.modifications[132]=valeur
			print(self.modifications)

	@pyqtSlot()
	def on_pushButtonAppliquer_clicked(self):
		for key, value in self.modifications.items():
			setting="${}={}\n".format(key, value)
			setting=setting.encode()
			self.connexion.write(setting)
			rx=self.connexion.readline().decode().strip()
		self.output.insertPlainText("ok")
		self.output.moveCursor(QTextCursor.End)
		self.output.ensureCursorVisible()
		if self.modifications[13]=="0":
			self.labelUnite_.setText("millimetre(mm)")
		else:
			self.labelUnite_.setText("pouce")
		self.close()

	def conversionBinaireDecimal(self, n):
		print("((((((((((((((((((((((", n)
		if n=="0":
			return 0
		if n=="1":
			return 1
		if n=="10":
			return 2
		if n=="11":
			return 3
		if n=="100":
			return 4
		if n=="101":
			return 5
		if n=="110":
			return 6
		if n=="111":
			return 7


	@pyqtSlot()
	def on_pushButtonAnnuler2_clicked(self):
		self.close()


	@pyqtSlot()
	def on_pushButtonRestaurer_clicked(self):
		self.connexion.write("$RST=$\n".encode())
		
		for _ in range(4):
			rx=self.connexion.readline().decode().strip()
			if rx=="ok":
				QMessageBox.information(self," ", "Configurations restaurées avec succes")
			self.output.insertPlainText(rx+"\n")
			self.output.moveCursor(QTextCursor.End)
			self.output.ensureCursorVisible()
		self.close()



			






















		





