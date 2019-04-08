
import os

from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QFont, QColor, QIcon, QKeySequence, QIntValidator, QImage, QTextListFormat
from PySide2.QtGui import QTextCharFormat
from PySide2.QtWidgets import QScrollArea, QWidget, QLabel, QLayout, QStackedWidget, QMenu, QVBoxLayout
from PySide2.QtWidgets import QHBoxLayout, QAction, QFontComboBox, QComboBox, QSizePolicy, QToolButton
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

		self.createActions()
		
		self.setFixedWidth(200)
		sizePolicy = QSizePolicy()
		sizePolicy.setVerticalPolicy(QSizePolicy.Expanding)
		sizePolicy.setHorizontalPolicy(QSizePolicy.Maximum)
		self.setSizePolicy(sizePolicy)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		self.stacked_widget = QStackedWidget()
		self.stacked_widget.setStyleSheet(""".QStackedWidget {
				background-color: transparent; 
				border: none ;
			} """)

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
		else:
			self.highlightActiveToolButton()

	def toggleVisibility(self):
		self.setVisible(not self.isVisible())
		self.highlightActiveToolButton()

	def highlightActiveToolButton(self):
		for index, action in enumerate(self.parent.tool_bar_actions, start=1):
			if (index == self.CURRENT_PAGE and self.isVisible()):
				action.setChecked(True)
			else:
				action.setChecked(False)

	def setThemeColor(self, themeColor):
		self.setStyleSheet(""" QScrollArea { 
				background-color: """ + themeColor  + """;
				border: none; 
				border-left: 1px solid white; 
			}""")

		self.verticalScrollBar().setStyleSheet(""" QScrollBar:vertical {
				border: none;
				background: """ + themeColor + """ ;
				width: 8px;
				margin: 0;
			}
			QScrollBar::handle:vertical {
				background: #8f8f8f;
				min-height: 20px;
				border-radius: 3px;
			}
			QScrollBar::handle:vertical:hover {
				background: white;
			}
			QScrollBar::add-line:vertical {
				border: none;
				background: """ + themeColor + """ ;
				height: 0px;
				subcontrol-position: bottom;
				subcontrol-origin: margin;
			}
			QScrollBar::sub-line:vertical {
				border: none;
				background: """ + themeColor + """ ;
				height: 0px;
				subcontrol-position: top;
				subcontrol-origin: margin;
			}
			QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
				border: none;
				width: 0px;
				height: 0px;
				background: white;
			}
			QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
				background: none;
			} """)

	def updateFormatWidgets(self, format):
		"""Responsible for updating font widgets when cursor position is changed.
		Checks for bold, italic, underline, font size, font family and font color in selected text. """

		if(format.fontPointSize()):
			self.formatPage.fontSizeCombo.setCurrentIndex(self.formatPage.fontSizeCombo.findText(str(int(format.fontPointSize()))))
		
		if(format.fontFamily()):
			self.formatPage.fontCombo.setCurrentIndex(self.formatPage.fontCombo.findText(str(format.fontFamily())))
		
		if(format.foreground()):
			self.formatPage.fontColorToolButton.setIcon(ColorUtils.createColorToolButtonIcon(qta.icon('fa5s.font'), format.foreground()))
		# elif(format.foreground() == Qt.NoBrush): # does not work
		# 	self.formatPage.fontColorToolButton.setIcon(ColorUtils.createColorToolButtonIcon(qta.icon('fa5s.font'), Qt.black))


		self.parent.edit_actions[0].setChecked(True if format.fontWeight() == QFont.Bold else False)
		self.parent.edit_actions[1].setChecked(format.fontItalic())
		self.parent.edit_actions[2].setChecked(format.fontUnderline())
		self.parent.more_edit_actions[0].setChecked(format.fontStrikeOut())
		align = format.verticalAlignment()
		self.parent.more_edit_actions[1].setChecked(True if align == QTextCharFormat.AlignSuperScript else False)
		self.parent.more_edit_actions[2].setChecked(True if align == QTextCharFormat.AlignSubScript else False)

	def updateIndentWidgets(self, alignment):
		"""Responsible for updating indent widgets."""

		indentID = GenUtils.getIndentID(alignment)
		for index, action in enumerate(self.parent.indent_actions, start=1):
			if(index == indentID):
				action.setChecked(True)
			else:
				action.setChecked(False)

	def updateListWidgets(self, listType):
		"""Responsible for updating list widgets."""

		listID = GenUtils.getListID(listType)
		for index, action in enumerate(self.parent.list_actions, start=1):
			if(index == listID):
				action.setChecked(True)
			else:
				action.setChecked(False)

	def createActions(self):
		self.parent.toggle_nav_action = QAction("Navigation", self.parent, shortcut="Ctrl+D", statusTip="Toggle Navigation")
		self.parent.toggle_nav_action.triggered.connect(self.toggleVisibility)
		self.parent.addAction(self.parent.toggle_nav_action)
            

class FormatPage(QWidget):
	def __init__(self, parent=None):
		super().__init__()

		self.parent = parent

		self.createActions()

		f_vlayout = QVBoxLayout()
		f_vlayout.setMargin(0)
		f_vlayout.setContentsMargins(0, 0, 0, 0)
		f_vlayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		f_vlayout.setDirection(QVBoxLayout.TopToBottom)
		f_vlayout.setSpacing(10)

		self.fontCombo = QFontComboBox()
		self.fontCombo.setEditable(False)
		self.fontCombo.currentFontChanged[QFont].connect(self.parent._fontFamily)
		self.fontCombo.setCurrentIndex(self.fontCombo.findText("Calibri"))
		
		self.fontSizeCombo = QComboBox()
		self.fontSizeCombo.setEditable(True)
		# self.fontSizeCombo.setMinimumContentsLength(4) #does not work
		for i in range(8, 60, 2):
			self.fontSizeCombo.addItem(str(i))
		validator = QIntValidator(2, 64, self.parent)
		self.fontSizeCombo.setValidator(validator)
		self.fontSizeCombo.currentIndexChanged[str].connect(self.parent._fontSize)
		self.fontSizeCombo.setCurrentIndex(2)
		
		self.fontColorToolButton = QToolButton()
		self.fontColorToolButton.setPopupMode(QToolButton.MenuButtonPopup)
		self.fontColorToolButton.setMenu(self.createColorMenu(self.textColorChanged, Qt.black))
		# self.textAction = self.fontColorToolButton.menu().defaultAction()
		self.fontColorToolButton.setIcon(ColorUtils.createColorToolButtonIcon(qta.icon('fa5s.font'), Qt.black))
		
		self.pageScaleCombo = QComboBox()
		self.pageScaleCombo.addItems(["A2", "A3Extra", "A3", "A4", "A5Extra", "A5"])
		self.pageScaleCombo.setCurrentIndex(4)
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
		
		self.moreEditBar = QWidget()
		moreEditLay = QHBoxLayout(self.moreEditBar)
		moreEditLay.setSizeConstraint(QLayout.SetFixedSize)
		for action in self.parent.more_edit_actions:
			self.parent.addAction(action) # prevents action from being disabled when navbar is hidden
			button = QToolButton()
			button.setDefaultAction(action)
			moreEditLay.addWidget(button)
		self.moreEditBar.setLayout(moreEditLay)

		self.indentBar = QWidget()
		indentLay = QHBoxLayout(self.indentBar)
		indentLay.setSizeConstraint(QLayout.SetFixedSize)
		for action in self.parent.indent_actions:
			self.parent.addAction(action) # prevents action from being disabled when navbar is hidden
			button = QToolButton()
			button.setDefaultAction(action)
			indentLay.addWidget(button)
		self.indentBar.setLayout(indentLay)

		self.listBar = QWidget()
		listLay = QHBoxLayout(self.listBar)
		listLay.setSizeConstraint(QLayout.SetFixedSize)
		for action in self.parent.list_actions:
			self.parent.addAction(action) # prevents action from being disabled when navbar is hidden
			button = QToolButton()
			button.setDefaultAction(action)
			listLay.addWidget(button)
		self.listBar.setLayout(listLay)

		f_vlayout.addWidget(NavTitle("Properties"))
		f_vlayout.addWidget(self.fontCombo)
		f_vlayout.addWidget(self.fontSizeCombo)
		f_vlayout.addWidget(self.fontColorToolButton)
		f_vlayout.addWidget(self.pageScaleCombo)
		f_vlayout.addWidget(self.editBar)
		f_vlayout.addWidget(self.moreEditBar)
		f_vlayout.addWidget(NavTitle("Paragraph"))
		f_vlayout.addWidget(self.indentBar)
		f_vlayout.addWidget(self.listBar)
		f_vlayout.addWidget(NavTitle("Show advanced options"))

		f_vlayout.addStretch(1)
		self.setLayout(f_vlayout)

	def createActions(self):
		# Actions grouped into tuples to ease display in navbar
		self.parent.edit_actions = (QAction(qta.icon('fa5s.bold'), "Bold", self.parent, checkable=True, shortcut=QKeySequence.Bold, triggered=self.parent._bold),
				QAction(qta.icon('fa5s.italic'), "Italic", self.parent, checkable=True, shortcut=QKeySequence.Italic, triggered=self.parent._italic),
				QAction(qta.icon('fa5s.underline'), "Underline", self.parent, checkable=True, shortcut=QKeySequence.Underline, triggered=self.parent._underline))
		self.parent.more_edit_actions = (QAction(qta.icon('fa5s.strikethrough'), "Strikethrough", self.parent, checkable=True, triggered=self.parent._strike),
				QAction(qta.icon('fa5s.superscript'), "Superscript", self.parent, checkable=True, triggered=self.parent._superscript),
				QAction(qta.icon('fa5s.subscript'), "Subscript", self.parent, checkable=True, triggered=self.parent._subscript))
		self.parent.indent_actions = (QAction(qta.icon('fa5s.align-left'), "Left", self.parent, checkable=True, shortcut="Ctrl+L", statusTip="Left indent", triggered=(lambda align=Qt.AlignLeft: self.parent._indent(align))),
				QAction(qta.icon('fa5s.align-right'), "Right", self.parent, checkable=True, shortcut="Ctrl+R", statusTip="Right indent", triggered=(lambda align=Qt.AlignRight: self.parent._indent(align))),
				QAction(qta.icon('fa5s.align-center'), "Center", self.parent, checkable=True, shortcut="Ctrl+E", statusTip="Center indent", triggered=(lambda align=Qt.AlignCenter: self.parent._indent(align))),
				QAction(qta.icon('fa5s.align-justify'), "Justify", self.parent, checkable=True, shortcut="Ctrl+J", statusTip="Justify indent", triggered=(lambda align=Qt.AlignJustify: self.parent._indent(align))))
		self.parent.list_actions = (QAction(qta.icon('fa5s.list-ul'), "Bullet List", self.parent, checkable=True, statusTip="Insert bullet List", triggered=(lambda ltype=QTextListFormat.ListDisc: self.parent._list(ltype))),
				QAction(qta.icon('fa5s.list-ol'), "Numbered List", self, checkable=True, statusTip="Insert numbered List", triggered=(lambda ltype=QTextListFormat.ListDecimal: self.parent._list(ltype))),
				QAction(qta.icon('fa5s.list-alt'), "Numbered List", self, checkable=True, statusTip="Insert numbered List", triggered=(lambda ltype=QTextListFormat.ListLowerRoman: self.parent._list(ltype))),
				QAction(qta.icon('fa5s.list'), "Numbered List", self, checkable=True, statusTip="Insert numbered List", triggered=(lambda ltype=QTextListFormat.ListLowerAlpha: self.parent._list(ltype))))

	def createColorMenu(self, slot, defaultColor):
		colors = [Qt.black, Qt.white, Qt.red, Qt.blue, Qt.yellow, Qt.green, Qt.gray]
		names = ["black", "white", "red", "blue", "yellow", "Green", "Gray"]

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

		s_vlayout = QVBoxLayout()
		s_vlayout.setMargin(0)
		s_vlayout.setContentsMargins(0, 0, 0, 0)
		s_vlayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		s_vlayout.setDirection(QVBoxLayout.TopToBottom)
		s_vlayout.setSpacing(6)

		s_vlayout.addWidget(NavTitle("Sections"))

		# TODO Add thumbnails of document sections

		s_vlayout.addStretch(1)
		self.setLayout(s_vlayout)

class ThemesPage(QWidget):
	def __init__(self, parent=None):
		super().__init__()

		self.parent = parent

		t_vlayout = QVBoxLayout()
		t_vlayout.setMargin(0)
		t_vlayout.setContentsMargins(0, 0, 0, 0)
		t_vlayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		t_vlayout.setDirection(QVBoxLayout.TopToBottom)
		t_vlayout.setSpacing(10)

		t_vlayout.addWidget(NavTitle("Themes"))

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
				qim = QImage(data, im.size[0], im.size[1], QImage.Format_RGBA8888)

				pixmap = QPixmap.fromImage(qim)
				theme_view = ThemeThumb()
				theme_view.setPixmap(pixmap)
				theme_view.clicked.connect(lambda tp=rel_path: self.parent.setTheme(tp))

				t_vlayout.addWidget(theme_view)

		# TODO Add extra bottom widget for use to use and get custom themes

		t_vlayout.addWidget(NavTitle("Select custom themes"))

		t_vlayout.addStretch(1)
		self.setLayout(t_vlayout)


class NavTitle(QLabel):

    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet(""" 
				color: white; 
				margin: 10px; 
				font-weight: 300; 
				font-family: Comic Sans MS; 
			""")

