
import os, sys

# TODO Use specific imports
from PySide2.QtCore import * # Qt
from PySide2.QtWidgets import * # QWidget, QScrollArea, QStackedWidget, QVBoxLayout, QSizePolicy
from PySide2.QtGui import *

from views import themethumb
from utils.colorutils import ColorUtils
from utils.genutils import GenUtils
from PIL import Image

class NavPanel(QScrollArea):

	CURRENT_PAGE = 0
	
	def __init__(self, parent=None):
		super(NavPanel, self).__init__()

		self.parent = parent
		
		self.setFixedWidth(200)
		sizePolicy = QSizePolicy()
		sizePolicy.setVerticalPolicy(QSizePolicy.Expanding)
		sizePolicy.setHorizontalPolicy(QSizePolicy.Maximum)
		self.setSizePolicy(sizePolicy)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		self.stacked_widget = QStackedWidget()
		self.stacked_widget.setStyleSheet(".QStackedWidget {background-color: transparent; border: none;}")

		self.formatPage = FormatPage(self.parent)
		self.sectionsPage = SectionsPage(self.parent)
		self.themesPage = ThemesPage(self.parent)
		
		self.stacked_widget.addWidget(self.formatPage)
		self.stacked_widget.addWidget(self.sectionsPage)
		self.stacked_widget.addWidget(self.themesPage)
		self.setCurrentPage(1)

		self.setWidget(self.stacked_widget)
		self.setWidgetResizable(True)

	def setCurrentPage(self, page):
		if(page == 1):
			self.stacked_widget.setCurrentWidget(self.formatPage)
		elif(page == 2):
			self.stacked_widget.setCurrentWidget(self.sectionsPage)
		elif(page == 3):
			self.stacked_widget.setCurrentWidget(self.themesPage)

		pageChanged = (page != self.CURRENT_PAGE)
		if(not self.isVisible()):
			pageChanged = False
		self.CURRENT_PAGE = page

		return pageChanged

	def toggleVisibility(self):
		self.setVisible(not self.isVisible())
            

class FormatPage(QWidget):
	def __init__(self, parent=None):
		super().__init__()

		self.parent = parent

		f_vlayout = QVBoxLayout()

		fontCombo = QFontComboBox()
		fontCombo.currentFontChanged.connect(self.parent._fontFamily)
		
		fontSizeCombo = QComboBox()
		fontSizeCombo.setEditable(True)
		for i in range(8, 30, 2):
			fontSizeCombo.addItem(str(i))
		validator = QIntValidator(2, 64, self.parent)
		fontSizeCombo.setValidator(validator)
		fontSizeCombo.currentIndexChanged.connect(self.parent._fontSize)
		
		fontColorToolButton = QToolButton()
		fontColorToolButton.setPopupMode(QToolButton.MenuButtonPopup)
		fontColorToolButton.setMenu(self.parent.createColorMenu(self.parent.textColorChanged, Qt.black))
		# self.textAction = fontColorToolButton.menu().defaultAction()
		fontColorToolButton.setIcon(ColorUtils.createColorToolButtonIcon('src/images/textpointer.png', Qt.black))
		# FIXME parameter is set to bool; get selected menu color and parse as argument
		fontColorToolButton.clicked.connect(self.parent.textButtonTriggered)
		
		pageScaleCombo = QComboBox()
		pageScaleCombo.addItems(["50%", "75%", "100%", "125%", "150%"])
		pageScaleCombo.setCurrentIndex(2)
		pageScaleCombo.currentIndexChanged[str].connect(self.parent.pageScaleChanged)

		editBar = QWidget()
		editLay = QHBoxLayout(editBar)
		editLay.setSizeConstraint(QLayout.SetFixedSize)
		# for action in self.parent.edit_actions:
		# 	self.parent.addAction(action) # prevents action from being disabled when navbar is hidden
		# 	button = QToolButton()
		# 	button.setDefaultAction(action)
		# 	editLay.addWidget(button)
		editBar.setLayout(editLay)

		indentBar = QWidget()
		indentLay = QHBoxLayout(indentBar)
		indentLay.setSizeConstraint(QLayout.SetFixedSize)
		# for action in self.parent.indent_actions:
		# 	self.parent.addAction(action) # prevents action from being disabled when navbar is hidden
		# 	button = QToolButton()
		# 	button.setDefaultAction(action)
		# 	indentLay.addWidget(button)
		indentBar.setLayout(indentLay)

		f_vlayout.addWidget(fontCombo)
		f_vlayout.addWidget(fontSizeCombo)
		f_vlayout.addWidget(fontColorToolButton)
		f_vlayout.addWidget(pageScaleCombo)
		f_vlayout.addWidget(editBar)
		f_vlayout.addWidget(indentBar)

		self.setLayout(f_vlayout)

class SectionsPage(QWidget):
	def __init__(self, parent=None):
		super().__init__()

		self.parent = parent

class ThemesPage(QWidget):
	def __init__(self, parent=None):
		super().__init__()

		self.parent = parent

		t_vlayout = QVBoxLayout()

		themedir = 'src/themes'
		for theme in os.listdir(themedir):
			rel_path = GenUtils.resource_path(os.path.join(themedir, theme))
			if os.path.isfile(rel_path):
				im = Image.open(rel_path)
				im.thumbnail((360, 360), Image.ANTIALIAS)

				# Convert PIL Image to QImage. The PIL ImageQT class failed to do this for me
				im = im.convert("RGBA")
				data = im.tobytes('raw', "RGBA")
				qim = QImage(data, im.size[0], im.size[1], QImage.Format_ARGB32)

				pixmap = QPixmap.fromImage(qim)
				theme_view = themethumb.ThemeThumb()
				theme_view.setPixmap(pixmap)
				theme_view.clicked.connect(lambda tp=rel_path: self.parent.setTheme(tp))

				t_vlayout.addWidget(theme_view)


		self.setLayout(t_vlayout)
