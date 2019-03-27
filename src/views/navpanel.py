
import os

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QScrollArea, QWidget, QLayout, QStackedWidget, QMenu, QVBoxLayout, QHBoxLayout, QAction, QFontComboBox, QComboBox, QSizePolicy, QToolButton
from PySide2.QtGui import QPixmap, QFont, QColor, QIcon, QKeySequence, QIntValidator, QImage
import qtawesome as qta
from views.themethumb import ThemeThumb
from utils.colorutils import ColorUtils
from utils.genutils import GenUtils
from PIL import Image

class NavPanel(QScrollArea):

	CURRENT_PAGE = 1
	
	def __init__(self, parent=None):
		super(NavPanel, self).__init__()

		self.parent = parent

		self.setObjectName("MyNavPanel")
		self.setStyleSheet("QScrollArea#MyNavPanel { border: none; border-left: 1px solid white; }")
		
		self.setFixedWidth(200)
		sizePolicy = QSizePolicy()
		sizePolicy.setVerticalPolicy(QSizePolicy.Expanding)
		sizePolicy.setHorizontalPolicy(QSizePolicy.Maximum)
		self.setSizePolicy(sizePolicy)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		self.stacked_widget = QStackedWidget()
		self.stacked_widget.setStyleSheet(".QStackedWidget {background-color: transparent; border: none ;}")

		self.formatPage = FormatPage(self.parent)
		self.sectionsPage = SectionsPage(self.parent)
		self.themesPage = ThemesPage(self.parent)
		
		self.stacked_widget.addWidget(self.formatPage)
		self.stacked_widget.addWidget(self.sectionsPage)
		self.stacked_widget.addWidget(self.themesPage)

		self.setWidget(self.stacked_widget)
		self.setWidgetResizable(True)

	def setCurrentPage(self, page=CURRENT_PAGE):
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

		if(not pageChanged):
			self.toggleVisibility()

		for index, action in enumerate(self.parent.tool_bar_actions, start=1):
			if (index == self.CURRENT_PAGE and self.isVisible()):
				action.setChecked(True)
			else:
				action.setChecked(False)

	def toggleVisibility(self):
		self.setVisible(not self.isVisible())

	def updateFormatWidgets(self, format):
		"""Responsible for updating font widgets when cursor position is changed.
		Checks for bold, italic, underline, font size, font family and font color in selected text. """

		self.formatPage.fontSizeCombo.setCurrentIndex(self.formatPage.fontSizeCombo.findText(str(int(format.fontPointSize()))))
		self.formatPage.fontCombo.setCurrentIndex(self.formatPage.fontCombo.findText(str(format.fontFamily())))
		self.formatPage.fontColorToolButton.setIcon(ColorUtils.createColorToolButtonIcon(qta.icon('fa5s.font'), format.foreground()))

		self.parent.edit_actions[0].setChecked(True if format.fontWeight() == QFont.Bold else False)
		self.parent.edit_actions[1].setChecked(format.fontItalic())
		self.parent.edit_actions[2].setChecked(format.fontUnderline())
            

class FormatPage(QWidget):
	def __init__(self, parent=None):
		super().__init__()

		self.parent = parent

		self.createActions()

		f_vlayout = QVBoxLayout()
		f_vlayout.setMargin(0)

		self.fontCombo = QFontComboBox()
		self.fontCombo.currentFontChanged[QFont].connect(self.parent._fontFamily)
		
		self.fontSizeCombo = QComboBox()
		self.fontSizeCombo.setEditable(True)
		for i in range(8, 30, 2):
			self.fontSizeCombo.addItem(str(i))
		validator = QIntValidator(2, 64, self.parent)
		self.fontSizeCombo.setValidator(validator)
		self.fontSizeCombo.currentIndexChanged[str].connect(self.parent._fontSize)
		
		self.fontColorToolButton = QToolButton()
		self.fontColorToolButton.setPopupMode(QToolButton.MenuButtonPopup)
		self.fontColorToolButton.setMenu(self.createColorMenu(self.textColorChanged, Qt.black))
		# self.textAction = self.fontColorToolButton.menu().defaultAction()
		self.fontColorToolButton.setIcon(ColorUtils.createColorToolButtonIcon(qta.icon('fa5s.font'), Qt.black))
		
		self.pageScaleCombo = QComboBox()
		self.pageScaleCombo.addItems(["50%", "75%", "100%", "125%", "150%"])
		self.pageScaleCombo.setCurrentIndex(2)
		self.pageScaleCombo.currentIndexChanged[str].connect(self.parent.pageScaleChanged)

		self.editBar = QWidget()
		editLay = QHBoxLayout(self.editBar)
		editLay.setSizeConstraint(QLayout.SetFixedSize)
		for action in self.parent.edit_actions:
			self.parent.addAction(action) # prevents action from being disabled when navbar is hidden
			button = QToolButton()
			button.setDefaultAction(action)
			editLay.addWidget(button)
		self.editBar.setLayout(editLay)

		self.indentBar = QWidget()
		indentLay = QHBoxLayout(self.indentBar)
		indentLay.setSizeConstraint(QLayout.SetFixedSize)
		for action in self.parent.indent_actions:
			self.parent.addAction(action) # prevents action from being disabled when navbar is hidden
			button = QToolButton()
			button.setDefaultAction(action)
			indentLay.addWidget(button)
		self.indentBar.setLayout(indentLay)

		f_vlayout.addWidget(self.fontCombo)
		f_vlayout.addWidget(self.fontSizeCombo)
		f_vlayout.addWidget(self.fontColorToolButton)
		f_vlayout.addWidget(self.pageScaleCombo)
		f_vlayout.addWidget(self.editBar)
		f_vlayout.addWidget(self.indentBar)

		self.setLayout(f_vlayout)

	def createActions(self):
		# Actions grouped into tuples to ease display in navbar
		self.parent.edit_actions = (QAction(qta.icon('fa5s.bold'), "Bold", self.parent, checkable=True, shortcut=QKeySequence.Bold, triggered=self.parent._bold),
				QAction(qta.icon('fa5s.italic'), "Italic", self.parent, checkable=True, shortcut=QKeySequence.Italic, triggered=self.parent._italic),
				QAction(qta.icon('fa5s.underline'), "Underline", self.parent, checkable=True, shortcut=QKeySequence.Underline, triggered=self.parent._underline))
		self.parent.indent_actions = (QAction(qta.icon('fa5s.align-left'), "Left", self.parent, checkable=True, statusTip="Left indent", triggered=(lambda align=Qt.AlignLeft: self.parent._indent(align))),
				QAction(qta.icon('fa5s.align-right'), "Right", self.parent, checkable=True, statusTip="Right indent", triggered=(lambda align=Qt.AlignRight: self.parent._indent(align))),
				QAction(qta.icon('fa5s.align-center'), "Center", self.parent, checkable=True, shortcut="Ctrl+E", statusTip="Center indent", triggered=(lambda align=Qt.AlignCenter: self.parent._indent(align))),
				QAction(qta.icon('fa5s.align-justify'), "Justify", self.parent, checkable=True, statusTip="Justify indent", triggered=(lambda align=Qt.AlignJustify: self.parent._indent(align))))

	def createColorMenu(self, slot, defaultColor):
		colors = [Qt.black, Qt.white, Qt.red, Qt.blue, Qt.yellow]
		names = ["black", "white", "red", "blue", "yellow"]

		colorMenu = QMenu(self)
		for color, name in zip(colors, names):
			action = QAction(ColorUtils.createColorIcon(color), name, self,
					triggered=slot)
			action.setData(QColor(color))
			colorMenu.addAction(action)
			if color == defaultColor:
				colorMenu.setDefaultAction(action)
		return colorMenu

	def textColorChanged(self):
		newColor = QColor(self.sender().data())
		self.fontColorToolButton.setIcon(ColorUtils.createColorToolButtonIcon(qta.icon('fa5s.font'), 
				newColor))
		self.parent._fontColor(newColor)
		

class SectionsPage(QWidget):
	def __init__(self, parent=None):
		super().__init__()

		self.parent = parent

class ThemesPage(QWidget):
	def __init__(self, parent=None):
		super().__init__()

		self.parent = parent

		t_vlayout = QVBoxLayout()
		t_vlayout.setMargin(0)

		themedir = GenUtils.resource_path('src/themes')
		for theme in os.listdir(themedir):
			# FIXME Dont call GenUtils.resource_path() twice
			rel_path = GenUtils.resource_path(os.path.join(themedir, theme))
			if os.path.isfile(rel_path):
				im = Image.open(rel_path)
				im.thumbnail((360, 360), Image.ANTIALIAS)

				# Convert PIL Image to QImage. The PIL ImageQT class failed to do this for me
				im = im.convert("RGBA")
				data = im.tobytes('raw', "RGBA")
				qim = QImage(data, im.size[0], im.size[1], QImage.Format_ARGB32)

				pixmap = QPixmap.fromImage(qim)
				theme_view = ThemeThumb()
				theme_view.setPixmap(pixmap)
				theme_view.clicked.connect(lambda tp=rel_path: self.parent.setTheme(tp))

				t_vlayout.addWidget(theme_view)

		# TODO Add extra bottom widget for use to use and get custom themes

		self.setLayout(t_vlayout)
