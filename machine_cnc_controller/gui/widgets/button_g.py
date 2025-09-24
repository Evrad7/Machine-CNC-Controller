"""Custom button updating its icon depending on mouse hover state."""

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

from machine_cnc_controller.resources import image_path


class ButtonG55(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.quitte = True

    def enterEvent(self, event):  # noqa: N802 (Qt override naming)
        self.setIcon(QIcon(image_path("G55E.PNG")))

    def leaveEvent(self, event):  # noqa: N802 (Qt override naming)
        if self.quitte:
            self.setIcon(QIcon(image_path("G55.PNG")))
