
from PySide2.QtCore import Qt, Signal, QPoint, QSize
from PySide2.QtGui import QPainter, QPixmap
from PySide2.QtWidgets import QWidget, QStackedWidget, QStyleOption, QStyle

class DropView(QStackedWidget):
	""" A widget for the application background
	which will contain the changing themes. """

	# drop = ""

	def __init__(self, *args):
		super().__init__(*args)

		self.setObjectName("MyDropView")

		# self.drop  = QPixmap()
	

	def paintEvent(self, _event):
		# if(not self.getDrop):
		# 	return
			
		painter = QPainter(self)
		# painter.setRenderHint(QPainter.Antialiasing)

		# scaledPix = self.getDrop().scaledToWidth(_event.rect().width())
		# painter.drawPixmap(self.rect(), scaledPix)

		super().paintEvent(_event)

	def getDrop(self):
		return self.drop

	def dropImage(self, imagePath):
		# pixmap = QPixmap(imagePath)
		# self.drop = pixmap

		self.setStyleSheet("QWidget#MyDropView { border-image: url(" + imagePath + ");}")
