
import math

from PySide2.QtCore import Qt, Signal, QPoint, QSize
from PySide2.QtGui import QPainter, QPixmap
from PySide2.QtWidgets import QWidget, QLabel, QSizePolicy

class ThemeLabel(QWidget):
	""" A Label for themes in the navbar.
	It emits a signal when clicked. """

	clicked = Signal()
	pix = ""

	def __init__(self, *args):
		super().__init__(*args)
		self.setFixedWidth(200)
		sizePolicy = QSizePolicy()
		sizePolicy.setVerticalPolicy(QSizePolicy.MinimumExpanding)
		sizePolicy.setHorizontalPolicy(QSizePolicy.Fixed)
		self.setSizePolicy(sizePolicy)
		self.hasHeightForWidth()

		self.pix  = QPixmap()
		self._heightForWidthFactor = 1.0

	def hasHeightForWidth(self):
		return True

	def heightForWidth(self, width):
		return math.ceil(width / 2)
	

	def paintEvent(self, _event):
		if(not self.pix):
			return
			
		painter = QPainter(self);
		painter.setRenderHint(QPainter.Antialiasing);

		pixSize = self.pix.size();
		pixSize.scale(_event.rect().size(), Qt.KeepAspectRatio);

		scaledPix = self.pix.scaled(pixSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)

		painter.drawPixmap(QPoint(), scaledPix)

		super().paintEvent(_event)

	def pixmap(self):
		return self.pix

	def setPixmap(self, pixmap):
		self.pix = pixmap

	def mousePressEvent(self, event):
		self.clicked.emit()