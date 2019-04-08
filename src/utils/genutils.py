import os
import sys

from PySide2.QtCore import Qt
from PySide2.QtGui import QPageSize, QTextListFormat

class GenUtils:
	"""This class contains general utility functions. """

	def resource_path(relative):
		""" Get absolute path to resource, works for dev and for PyInstaller """
		if hasattr(sys, "_MEIPASS"):
			path = os.path.join(sys._MEIPASS, relative)
		else:
			path = os.path.join(relative)

		return path.replace(os.sep, '/')
		

	def count_words(text):
		return (len(text.split()), len(text))

	def getIndentID(indent):

		if(indent == Qt.AlignRight):
			return 2
		elif(indent == Qt.AlignCenter):
			return 3
		elif(indent == Qt.AlignJustify):
			return 4
		else:
			return 1

	def getListID(list):

		if(list == QTextListFormat.ListDisc):
			return 1
		elif(list == QTextListFormat.ListDecimal):
			return 2
		elif(list == QTextListFormat.ListLowerRoman):
			return 3
		elif(list == QTextListFormat.ListNumberSuffix):
			return 4
		else:
			return 0

	def getPageFormatFromString(formatStr):

		if(formatStr == "A2"):
			return QPageSize.A2
		elif(formatStr == "A3"):
			return QPageSize.A3
		elif(formatStr == "A3Extra"):
			return QPageSize.A3Extra
		elif(formatStr == "A4"):
			return QPageSize.A4
		elif(formatStr == "A5"):
			return QPageSize.A5
		elif(formatStr == "A5Extra"):
			return QPageSize.A5Extra
		else:
			return QPageSize.A4
		
		