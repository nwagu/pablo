
from PySide2.QtWidgets import QToolBar, QAction
from PySide2.QtGui import QIcon
from PySide2.QtCore import QSize

import qtawesome as qta

from utils.genutils import GenUtils

class ToolBar(QToolBar):
	
	def __init__(self, parent=None):
		super(ToolBar, self).__init__()

		self.parent = parent

		self.setMovable(False)
		self.setIconSize(QSize(30, 30))
		self.setFixedWidth(45)

		self.setObjectName("MyToolBar")
		self.setStyleSheet("QToolBar#MyToolBar { background-color: transparent; border: none; } .QToolButton { margin-bottom: 10px; margin-top: 10px; } ")

		self.createActions()
		self.createTools()

	def createTools(self):
		self.addAction(self.parent.main_format_action)
		self.addAction(self.parent.main_sections_action)
		self.addAction(self.parent.main_themes_action)
		
	def createActions(self):
		self.parent.main_format_action = QAction(qta.icon('fa5s.file'), "&Format", self.parent, statusTip = "Format", triggered=(lambda page=1: self.parent.navSelectorClicked(page)))
		self.parent.main_sections_action = QAction(qta.icon('fa5s.music'), "&Sections", self.parent, statusTip = "Sections", triggered=(lambda page=2: self.parent.navSelectorClicked(page)))
		self.parent.main_themes_action = QAction(qta.icon('fa5s.camera'), "&Themes", self.parent, statusTip = "Themes", triggered=(lambda page=3: self.parent.navSelectorClicked(page)))
		
		# qta.icon('fa5.file', 'fa5s.camera', options=[{'scale_factor': 0.5, 'active': 'fa5s.balance-scale'}, {'color': 'red'}])