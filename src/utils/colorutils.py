
import struct
import numpy as np
import scipy
import scipy.misc
import scipy.cluster

from PySide2.QtGui import QPainter, QPixmap, QIcon
from PySide2.QtCore import Qt, QRect, QSize

class ColorUtils:
	"""This class contains utility functions for color. """

	def getDominantColorFromImage(im):
		NUM_CLUSTERS = 5
		
		im = im.resize((50, 50))  # optional, to reduce time
		ar = np.asarray(im)
		shape = ar.shape
		ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

		codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)

		vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
		counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

		index_max = scipy.argmax(counts)                    # find most frequent
		peak = codes[index_max]
		return '#%02x%02x%02x' % tuple(int(i) for i in peak)

	def createColorToolButtonIcon(icon, color):
		pixmap = QPixmap(50, 80)
		pixmap.fill(Qt.transparent)
		painter = QPainter(pixmap)
		image = icon.pixmap(QSize(50, 80))
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
		
		