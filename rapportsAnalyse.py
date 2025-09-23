from PyQt5.QtWidgets import QApplication, QMainWindow
from rapportsAnalyse_ui import Ui_Form
import sys
class Rapports(QMainWindow, Ui_Form):
	def __init__(self, rapport):
		super(Rapports, self).__init__()
		self.setupUi(self)
		self.rapport=rapport
		self.plainTextEdit.insertPlainText(self.rapport)
		print("dhgdgfdgfd")


if __name__=="__main__":
	app=QApplication(sys.argv)
	r=Rapports("gfdgfdgsgsgsghdhdhbtbtb")
	r.show()
	sys.exit(app.exec_())
