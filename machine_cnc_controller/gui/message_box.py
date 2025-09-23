"""Dialog allowing the user to edit work coordinate offsets."""

import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from .generated.message_box_ui import Ui_Systeme_de_coordonnees

class MessageBoxG(QMainWindow, Ui_Systeme_de_coordonnees):
	def __init__(self, parent):
		super(MessageBoxG, self).__init__()
		self.setupUi(self)
		self.parent=parent
		if self.parent.repereActif==self.parent.wco:
			self.checkBoxRepereActif.setChecked(True)
		self.parent.connexion.connexion.write("$#\n".encode())
		c=True
		tableX=[]
		while(c):
			tx=self.parent.connexion.connexion.read_until().decode()
			if tx.find("ok")>-1:
				c=False
				break
			tableX.append(tx)
		
		coordonnees_repere=tableX[int(parent.wco)-1]#Coordonnées du repere dont on a clicqué pour modifier
	
		debut_coordonnees_repere=coordonnees_repere.find(":")
		coordonnees_repere=coordonnees_repere[debut_coordonnees_repere+1:len(coordonnees_repere)-3]
		cx, cy, cz=coordonnees_repere.split(",")
		self.lineEditX.setText(cx)
		self.lineEditY.setText(cy)
		self.lineEditZ.setText(cz)
		titreFenetre="système de coordonnées G{}".format(int(self.parent.wco)+53)
		self.setWindowTitle(titreFenetre)



	@pyqtSlot()
	def on_pushButtonAnnuler_clicked(self):
		self.close()

	@pyqtSlot()
	def on_pushButtonOK_clicked(self):
		self.signal()

	def signal(self):
		try:
			float(self.lineEditX.text())
			float(self.lineEditY.text())
			float(self.lineEditZ.text())
		except:
			QMessageBox.information(self, "erreur", " Veillez entrer un nombre.")
		else:
			x=float(self.lineEditX.text())
			y=float(self.lineEditY.text())
			z=float(self.lineEditZ.text())
			wco=self.parent.wco
			write="G10L2P{}X{}Y{}Z{}\n".format(wco, x, y, z)
			write=write.encode()
			self.parent.connexion.connexion.write(write)
			print(self.parent.connexion.connexion.readline().decode())
			if self.checkBoxRepereActif.isChecked():
				wcoAnterieur=self.parent.repereActif
				self.parent.repereActif=wco
				if wcoAnterieur!=wco:
					activerLaCase(self.parent, wcoAnterieur)

				G=str(int(wco)+53)
				self.parent.connexion.connexion.write("G{}\n".format(G).encode())
				print(self.parent.connexion.connexion.readline().decode())
				self.parent.connexion.connexion.write("?".encode())
				tx=self.parent.connexion.connexion.readline().decode()+"\n"
				self.parent.affichageCoordonnees(tx)
			self.close()

	@pyqtSlot()
	def on_pushButton_clicked(self):
		self.lineEditX.setText(str(self.parent.lcdNumberXM.value()))
		self.lineEditY.setText(str(self.parent.lcdNumberYM.value()))
		self.lineEditZ.setText(str(self.parent.lcdNumberZM.value()))


def activerLaCase(param, repereAnterieur=None):

	if param.repereActif=="1":
		param.pushButtonG54.setIcon(QIcon("images/G54A.PNG"))
	elif param.repereActif=="2":
		param.pushButtonG55.setIcon(QIcon("images/G55A.PNG"))
	elif param.repereActif=="3":
		param.pushButtonG56.setIcon(QIcon("images/G56A.PNG"))
	elif param.repereActif=="4":
		param.pushButtonG57.setIcon(QIcon("images/G57A.PNG"))
	elif param.repereActif=="5":
		param.pushButtonG58.setIcon(QIcon("images/G58A.PNG"))
	elif param.repereActif=="6":
		param.pushButtonG59.setIcon(QIcon("images/G59A.PNG"))

	if repereAnterieur!=None:
		if repereAnterieur=="1":
			param.pushButtonG54.setIcon(QIcon("images/G54.PNG"))
		if repereAnterieur=="2":
			param.pushButtonG55.setIcon(QIcon("images/G55.PNG"))
		if repereAnterieur=="3":
			param.pushButtonG56.setIcon(QIcon("images/G56.PNG"))
		if repereAnterieur=="4":
			param.pushButtonG57.setIcon(QIcon("images/G57.PNG"))
		if repereAnterieur=="5":
			param.pushButtonG58.setIcon(QIcon("images/G58.PNG"))
		if repereAnterieur=="6":
			param.pushButtonG59.setIcon(QIcon("images/G59.PNG"))
	
	
	
	
	




			
	

		

if __name__=="__main__":
	app=QApplication(sys.argv)
	m=MessageBoxG()
	m.show()
	sys.exit(app.exec_())


