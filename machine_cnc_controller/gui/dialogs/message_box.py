"""Dialog allowing the user to edit work coordinate offsets."""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from machine_cnc_controller.resources import image_path

from ..forms.message_box_ui import Ui_Systeme_de_coordonnees

_COORDINATE_BUTTONS = {
        "1": ("pushButtonG54", "G54"),
        "2": ("pushButtonG55", "G55"),
        "3": ("pushButtonG56", "G56"),
        "4": ("pushButtonG57", "G57"),
        "5": ("pushButtonG58", "G58"),
        "6": ("pushButtonG59", "G59"),
}

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

        for repere, (attribute, prefix) in _COORDINATE_BUTTONS.items():
                bouton = getattr(param, attribute, None)
                if bouton is None:
                        continue

                if param.repereActif == repere:
                        bouton.setIcon(QIcon(image_path(f"{prefix}A.PNG")))
                elif repereAnterieur == repere:
                        bouton.setIcon(QIcon(image_path(f"{prefix}.PNG")))
	
	
	
	
	




			
	

