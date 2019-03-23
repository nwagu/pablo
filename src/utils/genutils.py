import os
import sys

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
		