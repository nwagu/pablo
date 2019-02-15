import sys

from PySide2.QtWidgets import QWidget, QTextEdit, QGridLayout
from PySide2.QtGui import QColor, QPalette, QFont
from PySide2 import QtCore

class PabloView(QWidget):

    def __init__(self):
        super(PabloView, self).__init__()

        # self.setPalette(QPalette(QColor(105, 105, 105)))
        # self.setAutoFillBackground(True)

        self.grid = QGridLayout()
        self.text_edit = QTextEdit()
        self.side_edit = QTextEdit()
        self.text_edit.setText('Hello')
        font = QFont()
        font.setPointSize(20)
        font.setFamily('Calibri')
        self.text_edit.setFont(font)
        self.grid.addWidget(self.text_edit, 0, 0)
        self.grid.addWidget(self.side_edit, 0, 1)
        self.setLayout(self.grid)
