import sys

from PySide2.QtGui import QPageSize
from PySide2.QtCore import QSizeF, QMarginsF

class PageMetrics():

	m_pageFormat = QPageSize.PageSizeId()
	m_mmPageSize = QSizeF()
	m_mmPageMargins = QMarginsF()
	m_pxPageSize = QSizeF()
	m_pxPageMargins = QMarginsF()

	def __init__(self):
		super(PageMetrics, self).__init__()

	def mmToInches(self, mm):
		return mm * 0.039370147

	def mmToPx(self, _mm, _x):
		return self.mmToInches(_mm) * (qApp.desktop().logicalDpiX() if _x else qApp.desktop().logicalDpiY())

	def pageSizeIdFromString(self, _from):
		result = QPageSize.A4

		if (_from == "A0"):
			 result = QPageSize.A0
		elif (_from == "A1"):
			 result = QPageSize.A1
		elif (_from == "A2"):
			 result = QPageSize.A2
		elif (_from == "A3"):
			 result = QPageSize.A3
		elif (_from == "A4"):
			 result = QPageSize.A4
		elif (_from == "A5"):
			 result = QPageSize.A5
		elif (_from == "A6"):
			 result = QPageSize.A6
		else:
			Q_ASSERT_X(0, Q_FUNC_INFO, qPrintable("Undefined page size: " + _from))

		return result

	def stringFromPageSizeId(self, _pageSize):
		result = ""

		if(_pageSize == QPageSize.A0):
			result = "A0"
		elif (_pageSize == QPageSize.A1):
			result = "A1"
		elif (_pageSize == QPageSize.A2):
			result = "A2"
		elif (_pageSize == QPageSize.A3):
			result = "A3"
		elif (_pageSize == QPageSize.A4):
			result = "A4"
		elif (_pageSize == QPageSize.A5):
			result = "A5"
		elif (_pageSize == QPageSize.A6):
			result = "A6"
		else:
			Q_ASSERT_X(0, Q_FUNC_INFO, qPrintable("Undefined page size: " + QString.number(_pageSize)))
			
		return result

	def update(self, _pageFormat, _mmPageMargins=QMarginsF()):
		self.m_pageFormat = _pageFormat

		self.m_mmPageSize = QPageSize(self.m_pageFormat).rect(QPageSize.Millimeter).size()
		self.m_mmPageMargins = _mmPageMargins

		# Calculate values in pixels
		x = True; y = False
		self.m_pxPageSize = QSizeF(self.mmToPx(self.m_mmPageSize.width(), x), self.mmToPx(self.m_mmPageSize.height(), y))
		self.m_pxPageMargins = QMarginsF(self.mmToPx(self.m_mmPageMargins.left(), x), self.mmToPx(self.m_mmPageMargins.top(), y), self.mmToPx(self.m_mmPageMargins.right(), x), self.mmToPx(self.m_mmPageMargins.bottom(), y))

	def pageFormat(self):
		return self.m_pageFormat

	def mmPageSize(self):
		return self.m_mmPageSize

	def mmPageMargins(self):
		return self.m_mmPageMargins

	def pxPageSize(self):
		return QSizeF(self.m_pxPageSize.width(), self.m_pxPageSize.height())

	def pxPageMargins(self):
		return QMarginsF(self.m_pxPageMargins.left(), self.m_pxPageMargins.top(), self.m_pxPageMargins.right(), self.m_pxPageMargins.bottom())
