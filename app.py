from TML_sender_gcode import *
from PyQt5.QtWidgets import QApplication
import sys

app=QApplication(sys.argv)
mainWindowSender=MainWindowSender()

mainWindowSender.show()

sys.exit(app.exec_())

