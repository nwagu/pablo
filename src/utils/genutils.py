import os
import sys

from PySide2.QtCore import Qt

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
		return (str(len(text.split())), str(len(text)))

	def getIndentID(indent):

		if(indent == Qt.AlignRight):
			return 2
		elif(indent == Qt.AlignCenter):
			return 3
		elif(indent == Qt.AlignJustify):
			return 4
		else:
			return 1
		
		