
from PySide2.QtGui import *
from PySide2.QtCore import *

class ColorUtils:
	"""This class contains utility functions for color. """

	def createColorToolButtonIcon(imageFile, color):
		pixmap = QPixmap(50, 80)
		pixmap.fill(Qt.transparent)
		painter = QPainter(pixmap)
		image = QPixmap(imageFile)
		target = QRect(0, 0, 50, 60)
		source = QRect(0, 0, 42, 42)
		painter.fillRect(QRect(0, 60, 50, 80), color)
		painter.drawPixmap(target, image, source)
		painter.end()

		return QIcon(pixmap)

	def createColorIcon(color):
		pixmap = QPixmap(20, 20)
		painter = QPainter(pixmap)
		painter.setPen(Qt.NoPen)
		painter.fillRect(QRect(0, 0, 20, 20), color)
		painter.end()

		return QIcon(pixmap)
		
		