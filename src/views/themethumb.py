
from PySide2.QtCore import Qt, Signal, QPoint, QSize
from PySide2.QtGui import QPainter, QPixmap
from PySide2.QtWidgets import QWidget, QSizePolicy

class ThemeThumb(QWidget):
	""" A widget for themes in the navbar.
	It emits a signal when clicked. """

	clicked = Signal()
	pix = ""

	def __init__(self, *args):
		super().__init__(*args)
		self.setFixedWidth(200)
		sizePolicy = QSizePolicy()
		sizePolicy.setHorizontalPolicy(QSizePolicy.Maximum)
		sizePolicy.setVerticalPolicy(QSizePolicy.Expanding)
		self.setSizePolicy(sizePolicy)
		self.hasHeightForWidth()

		self.pix  = QPixmap()
		# self._heightForWidthFactor = 1.0

	def hasHeightForWidth(self):
		return True

	def heightForWidth(self, width):
		if(self.pixmap()):
			return int(width * self.pixmap().height() / self.pixmap().width())
		else:
			return width
	

	def paintEvent(self, _event):
		if(not self.pix):
			return
			
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		scaledPix = self.pixmap().scaledToWidth(_event.rect().width())
		painter.drawPixmap(QPoint(), scaledPix)

		super().paintEvent(_event)

	def pixmap(self):
		return self.pix

	def setPixmap(self, pixmap):
		self.pix = pixmap

	def mousePressEvent(self, event):
		self.clicked.emit()