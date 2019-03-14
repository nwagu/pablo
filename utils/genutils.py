import os
import sys

class GenUtils:
	"""This class contains general utility functions. """

	def resource_path(relative):
		if hasattr(sys, "_MEIPASS"):
			return os.path.join(sys._MEIPASS, relative)
		return os.path.join(relative)
		
	def resource_path2(relative_path):
		""" Get absolute path to resource, works for dev and for PyInstaller """
		try:
			# PyInstaller creates a temp folder and stores path in _MEIPASS
			base_path = sys._MEIPASS
		except AttributeError:
			base_path = os.path.abspath(".")

		return os.path.join(base_path, relative_path)
		