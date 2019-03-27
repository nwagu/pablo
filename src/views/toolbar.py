
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
		self.setStyleSheet("QToolBar#MyToolBar { background-color: transparent; border: none; } .QToolButton { margin-bottom: 15px; margin-top: 10px; border: none; } ")

		self.createActions()
		self.createTools()

	def createTools(self):
		for action in self.parent.tool_bar_actions:
			self.addAction(action)
		
	def createActions(self):
		format_icon = qta.icon('fa5s.keyboard', selected='fa5s.keyboard', color_off='gray', color_off_active='white', color_on='white', color_on_active='white')
		sections_icon = qta.icon('fa5s.book-open', selected='fa5s.book-open', color_off='gray', color_off_active='white', color_on='white', color_on_active='white')
		themes_icon = qta.icon('fa5s.images', selected='fa5s.images', color_off='gray', color_off_active='white', color_on='white', color_on_active='white')

		self.parent.tool_bar_actions = (QAction(format_icon, "&Format", self.parent, checkable=True, statusTip = "Format", triggered=(lambda page=1: self.parent.navSelectorClicked(page))),
				QAction(sections_icon, "&Sections", self.parent, checkable=True, statusTip = "Sections", triggered=(lambda page=2: self.parent.navSelectorClicked(page))),
				QAction(themes_icon, "&Themes", self.parent, checkable=True, statusTip = "Themes", triggered=(lambda page=3: self.parent.navSelectorClicked(page))))
	