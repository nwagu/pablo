from PySide2.QtCore import Signal
from PySide2.QtWidgets import QLabel

class ClickableLabel(QLabel):
    """ A Label that emits a signal when clicked. """

    clicked = Signal()

    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet(" color: white; font-weight: 800; ")
		

    def mousePressEvent(self, event):
        self.clicked.emit()