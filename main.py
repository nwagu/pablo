
import struct
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
from pagedtextedit import PagedTextEdit
from utils import Utils
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtPrintSupport import QPrintDialog, QPrinter
from PIL import Image

main_windows = []
m_theme = "themes/13.jpg"

def create_main_window(): # TODO this function should require a theme attribute
	"""Creates a MainWindow."""
	main_win = MainWindow()
	main_win._setup_components()
	main_win.setTheme(m_theme)
	main_windows.append(main_win)
	main_win.show()
	return main_win

class NavBar(QScrollArea):
	
	def __init__(self):
		super(NavBar, self).__init__()
		
		self.setFixedWidth(200)
		sizePolicy = QSizePolicy()
		sizePolicy.setVerticalPolicy(QSizePolicy.Expanding)
		sizePolicy.setHorizontalPolicy(QSizePolicy.Maximum)
		self.setSizePolicy(sizePolicy)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.vLayout = QVBoxLayout(self)
		self.setLayout(self.vLayout)
		
	def addComponent(self, component):
		self.vLayout.addWidget(component)
		
	def clearNavBar(self):
		pass # remove all widgets
		

class MainWindow(QMainWindow):
	"""Contains a menubar, statusbar
	also contains a QWidget, container, as central widget
	container contains the PagedTextEdit. """
	def __init__(self, fileName=None):
		super(MainWindow, self).__init__()

		self.curFile = ''
		self.curPage = (0, 0) # Tuple containing current page and total pages of the current file

		self.setWindowTitle('Pablo Editor')
		self.setWindowIcon(QIcon('images/icon.png'))
		self.setWindowState(Qt.WindowFullScreen)
		self.setWindowState(Qt.WindowMaximized)
		available_geometry = app.desktop().availableGeometry(self)
		self.resize(available_geometry.width(), available_geometry.height())
		self.readSettings()

		self.container = QWidget()

		self.paged_text_edit = PagedTextEdit(self.container)
		# The textedit must be transparent; the white pages are painted in paintEvent() function
		self.paged_text_edit.setStyleSheet("QTextEdit { background-color: transparent }")

		self.paged_text_edit.setFrameStyle(QFrame.NoFrame) # Removes a border-like line around the TextEdit

		doc = QTextDocument()
		font = QFont()
		font.setPointSize(12)
		font.setFamily('Calibri')
		doc.setDefaultFont(font)
		self.paged_text_edit.setDocument(doc)
		self.paged_text_edit.setPageFormat(QPageSize.A5Extra)
		self.paged_text_edit.setPageMargins(QMarginsF(15, 15, 15, 15))
		self.paged_text_edit.setUsePageMode(True)
		self.paged_text_edit.setPageNumbersAlignment(Qt.AlignBottom | Qt.AlignCenter)

		self.nav_bar = NavBar()
		# self.nav_bar.setVisible(False)
		self.setup_nav_bar()

		self.text_edit_layout = QHBoxLayout()
		self.text_edit_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.text_edit_layout.addWidget(self.nav_bar)
		self.text_edit_layout.setMargin(0)
		self.paged_text_edit.setLayout(self.text_edit_layout)

		# This below block of code prevents undoing the setDocumentMargin() and setFrameformat()
		# methods in the aboutUpdateDocumentGeometry function
		self.paged_text_edit.aboutUpdateDocumentGeometry()
		# self.paged_text_edit.document().clearUndoRedoStack() # This does not work
		# These commands work
		self.paged_text_edit.document().setUndoRedoEnabled(False)
		self.paged_text_edit.document().setUndoRedoEnabled(True)

		self.layout = QHBoxLayout()
		self.layout.addWidget(self.paged_text_edit)
		self.layout.setMargin(0)
		self.container.setLayout(self.layout)
		self.setCentralWidget(self.container)

		self.setCurrentFile('')
		self.paged_text_edit.document().contentsChanged.connect(self.documentWasModified)

	def _setup_components(self):
		self._create_menus()
		self._create_actions()
		self._create_tool_bar()
		self._create_status_bar()
		self.setStatusBar(self.statusBar)
		self.printMessageOnStatus("Ready", 10000)
		self.paged_text_edit.pageInfo.connect(self.readPageInfo)

		self.file_menu.addAction(self.new_action)
		self.file_menu.addAction(self.open_action)
		self.file_menu.addAction(self.save_action)
		self.file_menu.addAction(self.save_as_action)
		self.file_menu.addSeparator()
		self.file_menu.addAction(self.print_action)
		self.file_menu.addSeparator()
		self.file_menu.addAction(self.exit_action)

		self.edit_menu.addAction(self.font_action)
		self.edit_menu.addAction(self.cut_action)
		self.edit_menu.addAction(self.copy_action)
		self.edit_menu.addAction(self.paste_action)
		self.edit_menu.addSeparator()
		self.edit_menu.addAction(self.undo_action)
		self.edit_menu.addAction(self.redo_action)
		self.edit_menu.addSeparator()
		self.edit_menu.addAction(self.select_all_action)
		
		self.themes_menu.addAction(self.themes_action)
		self.about_menu.addAction(self.about_action)

		self.main_tool_bar.addAction(self.first_action)
		self.main_tool_bar.addAction(self.second_action)
		self.main_tool_bar.addAction(self.third_action)
		self.main_tool_bar.addAction(self.fourth_action)
		self.main_tool_bar.addAction(self.fifth_action)

		self.main_tool_bar.addAction(self.bold_action)
		self.main_tool_bar.addAction(self.italic_action)
		self.main_tool_bar.addAction(self.underline_action)

	def setup_nav_bar(self):
		self.fontCombo = QFontComboBox()
		self.fontCombo.currentFontChanged.connect(self.currentFontChanged)
		self.nav_bar.addComponent(self.fontCombo)
		
		self.fontSizeCombo = QComboBox()
		self.fontSizeCombo.setEditable(True)
		for i in range(8, 30, 2):
			self.fontSizeCombo.addItem(str(i))
		validator = QIntValidator(2, 64, self)
		self.fontSizeCombo.setValidator(validator)
		self.fontSizeCombo.currentIndexChanged.connect(self.fontSizeChanged)
		self.nav_bar.addComponent(self.fontSizeCombo)
		
		self.fontColorToolButton = QToolButton()
		self.fontColorToolButton.setPopupMode(QToolButton.MenuButtonPopup)
		self.fontColorToolButton.setMenu(self.createColorMenu(self.textColorChanged, Qt.black))
		self.textAction = self.fontColorToolButton.menu().defaultAction()
		self.fontColorToolButton.setIcon(Utils.createColorToolButtonIcon('images/textpointer.png', Qt.black))
		self.fontColorToolButton.setAutoFillBackground(True)

		# FIXME parameter is set to bool; get selected menu color and parse as argument
		self.fontColorToolButton.clicked.connect(self.textButtonTriggered)
		self.nav_bar.addComponent(self.fontColorToolButton)
		
		self.pageScaleCombo = QComboBox()
		self.pageScaleCombo.addItems(["50%", "75%", "100%", "125%", "150%"])
		self.pageScaleCombo.setCurrentIndex(2)
		self.pageScaleCombo.currentIndexChanged[str].connect(self.pageScaleChanged)
		self.nav_bar.addComponent(self.pageScaleCombo)

	def _create_actions(self):
		self.new_action  = QAction(QIcon('images/new.png'), "&New", self, shortcut=QKeySequence.New, statusTip="Create a New File", triggered=self.newFile)
		self.open_action = QAction(QIcon('images/open.png'), "O&pen", self, shortcut=QKeySequence.Open, statusTip="Open an existing file", triggered=self.open)
		self.save_action = QAction(QIcon('images/save.png'), "&Save", self, shortcut=QKeySequence.Save, statusTip="Save the current file to disk", triggered=self.save)
		self.save_as_action = QAction(QIcon('images/save.png'), "Save &As...", self, shortcut=QKeySequence.SaveAs, statusTip="Save the current file under a new name", triggered=self.saveAs)
		self.print_action = QAction(QIcon('images/print.png'), "&Print...", self, shortcut=QKeySequence.Print, statusTip="Print the current file", triggered=self.print_)
		self.exit_action = QAction(QIcon.fromTheme("application-exit"), "E&xit", self, shortcut="Ctrl+Q", statusTip="Exit the Application", triggered=self.close)
		self.cut_action = QAction(QIcon('images/cut.png'), "C&ut", self, shortcut=QKeySequence.Cut, statusTip="Cut the current selection to clipboard", triggered=self.paged_text_edit.cut)
		self.copy_action = QAction(QIcon('images/copy.png'), "C&opy", self, shortcut=QKeySequence.Copy, statusTip="Copy the current selection to clipboard", triggered=self.paged_text_edit.copy)
		self.paste_action = QAction(QIcon('images/paste.png'), "&Paste", self, shortcut=QKeySequence.Paste, statusTip="Paste the clipboard's content in current location", triggered=self.paged_text_edit.paste)
		self.select_all_action = QAction(QIcon('images/selectAll.png'), "Select All", self, statusTip="Select All", triggered=self.paged_text_edit.selectAll)
		self.redo_action = QAction(QIcon('images/redo.png'),"Redo", self, shortcut=QKeySequence.Redo, statusTip="Redo previous action", triggered=self.paged_text_edit.redo)
		self.undo_action = QAction(QIcon('images/undo.png'),"Undo", self, shortcut=QKeySequence.Undo, statusTip="Undo previous action", triggered=self.paged_text_edit.undo)
		
		self.themes_action = QAction(QIcon('images/save.png'), "&Themes...", self, statusTip = "Themes", triggered = self.fontChange)
		
		self.font_action = QAction("F&ont", self, statusTip = "Modify font properties", triggered = self.fontChange)
		
		self.bold_action = QAction(QIcon('images/bold.png'),"Bold", self, checkable=True, 
				shortcut=QKeySequence.Bold, triggered=self.handleFontChange)
		self.italic_action = QAction(QIcon('images/italic.png'), "Italic", self, checkable=True, 
				shortcut=QKeySequence.Italic, triggered=self.handleFontChange)
		self.underline_action = QAction(QIcon('images/underline.png'), "Underline", self, checkable=True, 
				shortcut=QKeySequence.Underline, triggered=self.handleFontChange)

		self.about_action = QAction(QIcon('images/about.png'), 'A&bout', self, shortcut = QKeySequence(QKeySequence.HelpContents), triggered=self.about_pablo)

		# Side toolbar actions...
		self.first_action = QAction(QIcon('images/arrow.png'), "&Side1", self, statusTip = "ph", triggered=self.toggleNavigationBar)
		self.second_action = QAction(QIcon('images/music.png'), "&Side2", self, statusTip = "ph", triggered=self.toggleNavigationBar)
		self.third_action = QAction(QIcon('images/palm.png'), "&Side3", self, statusTip = "ph", triggered=self.toggleNavigationBar)
		self.fourth_action = QAction(QIcon('images/sick.png'), "&Side4", self, statusTip = "ph", triggered=self.toggleNavigationBar)
		self.fifth_action = QAction(QIcon('images/theme.png'), "&Side5", self, statusTip = "ph", triggered=self.toggleNavigationBar)
		
		self.cut_action.setEnabled(False)
		self.copy_action.setEnabled(False)
		self.undo_action.setEnabled(False)
		self.redo_action.setEnabled(False)
		self.paged_text_edit.copyAvailable.connect(self.cut_action.setEnabled)
		self.paged_text_edit.copyAvailable.connect(self.copy_action.setEnabled)
		self.paged_text_edit.undoAvailable.connect(self.undo_action.setEnabled)
		self.paged_text_edit.redoAvailable.connect(self.redo_action.setEnabled)

	def _create_tool_bar(self):
		self.main_tool_bar = QToolBar()
		self.addToolBar(Qt.LeftToolBarArea, self.main_tool_bar)
		self.main_tool_bar.setMovable(False)
		self.main_tool_bar.setIconSize(QSize(30, 30));
		self.main_tool_bar.setFixedWidth(45);

	def _create_menus(self):
		self.file_menu = self.menuBar().addMenu("&File")
		self.edit_menu = self.menuBar().addMenu("&Edit")
		self.themes_menu = self.menuBar().addMenu("&Themes")
		self.about_menu = self.menuBar().addMenu("&About")

	def _create_status_bar(self):
		self.statusBar = QStatusBar()
		self.pageInfoStatusLabel = QLabel()
		self.statusBar.addPermanentWidget(self.pageInfoStatusLabel)

	def newFile(self):
		if self.maybeSave():
			self.paged_text_edit.clear()
			self.setCurrentFile('')

	def open(self):
		fileName, filtr = QFileDialog.getOpenFileName(self, "Open File", 
				QDir.currentPath() + "/files", "PBL Files (*.pbl *.html)")
		if fileName:
			if self.maybeSave():
				self.loadFile(fileName)

	def save(self):
		if self.curFile:
			return self.saveFile(self.curFile)

		return self.saveAs()

	def saveAs(self):
		fileName, filtr = QFileDialog.getSaveFileName(self, "Save File", 
				QDir.currentPath() + "/files", "PBL Files (*.pbl)")
		if fileName:
			return self.saveFile(fileName)

		return False

	def loadFile(self, fileName):
		file = QFile(fileName)
		if not file.open(QFile.ReadOnly | QFile.Text):
			QMessageBox.warning(self, "Pablo",
					"Cannot read file %s:\n%s." % (fileName, file.errorString()))
			return

		inFile = QTextStream(file)
		QApplication.setOverrideCursor(Qt.WaitCursor)

		if (QFileInfo(fileName).suffix() in ("pbl", "html")):
			# TODO Write a custom QtextEdit.setPbl() function
			self.paged_text_edit.setHtml(inFile.readAll())
		else:
			self.paged_text_edit.setPlainText(inFile.readAll())

		QApplication.restoreOverrideCursor()

		self.setCurrentFile(fileName)
		self.printMessageOnStatus("File loaded", 2000)

	def saveFile(self, fileName):
		file = QFile(fileName)
		if not file.open(QFile.WriteOnly | QFile.Text):
			QMessageBox.warning(self, "Pablo",
					"Cannot write file %s:\n%s." % (fileName, file.errorString()))
			return False

		outFile = QTextStream(file)
		QApplication.setOverrideCursor(Qt.WaitCursor)

		if (QFileInfo(fileName).suffix() in ("pbl", "html")):
			# TODO Write a custom QtextEdit.toPbl() function
			# FIXME: Once file is out of scope, the file is empty, instead of having text.
			outFile << self.paged_text_edit.toHtml()
		else:
			outFile << self.paged_text_edit.toPlainText()
		
		QApplication.restoreOverrideCursor()

		self.setCurrentFile(fileName)
		self.statusBar.showMessage("File saved", 2000)
		return True

	def maybeSave(self):
		if self.paged_text_edit.document().isModified():
			ret = QMessageBox.warning(self, "Pablo",
					"The document has been modified.\nDo you want to save "
					"your changes?",
					QMessageBox.Save | QMessageBox.Discard |
					QMessageBox.Cancel)
			if ret == QMessageBox.Save:
				return self.save()
			elif ret == QMessageBox.Cancel:
				return False
		return True

	def setCurrentFile(self, fileName):
		self.curFile = fileName
		self.paged_text_edit.document().setModified(False)
		self.setWindowModified(False)

		if self.curFile:
			shownName = self.strippedName(self.curFile)
		else:
			shownName = "Untitled"

		self.setWindowTitle("%s[*] | Pablo" % shownName)

	def print_(self):
		document = self.paged_text_edit.document()
		printer = QPrinter()

		dlg = QPrintDialog(printer, self)
		if dlg.exec_() != QDialog.Accepted:
			return

		document.print_(printer)

		self.printMessageOnStatus("Ready", 2000)

	def strippedName(self, fullFileName):
		return QFileInfo(fullFileName).fileName()

	def fontChange(self):
		(font, ok) = QFontDialog.getFont(QFont("Helvetica[Cronyx]", 10), self)
		if ok:
			self.paged_text_edit.setCurrentFont(font)
	
	def closeEvent(self, event):
		if self.maybeSave():
			self.writeSettings()
			event.accept()
		else:
			event.ignore()

	def readSettings(self):
		settings = QSettings("Trolltech", "Application Example")
		pos = settings.value("pos", QPoint(200, 200))
		size = settings.value("size", QSize(400, 400))
		self.resize(size)
		self.move(pos)

	def writeSettings(self):
		settings = QSettings("Trolltech", "Application Example")
		settings.setValue("pos", self.pos())
		settings.setValue("size", self.size())

	def handleFontChange(self):

		format = QTextCharFormat()
		format.setFont(self.fontCombo.currentFont())
		format.setFontPointSize(int(self.fontSizeCombo.currentText()))
		if self.bold_action.isChecked():
			format.setFontWeight(QFont.Bold)
		else:
			format.setFontWeight(QFont.Normal)
		format.setFontItalic(self.italic_action.isChecked())
		format.setFontUnderline(self.underline_action.isChecked())

		self.paged_text_edit.mergeCurrentCharFormat(format)
		

	def currentFontChanged(self, font):
		self.handleFontChange()

	def fontSizeChanged(self, font):
		self.handleFontChange()

	def pageScaleChanged(self, scale):
		pass

	def textColorChanged(self):
		newColor = QColor(self.sender().data())
		self.fontColorToolButton.setIcon(Utils.createColorToolButtonIcon('images/textpointer.png', 
				newColor))
		self.textButtonTriggered(newColor)

	def textButtonTriggered(self, color):
		format = QTextCharFormat()
		format.setForeground(color)
		self.paged_text_edit.mergeCurrentCharFormat(format)

	def createColorMenu(self, slot, defaultColor):
		colors = [Qt.black, Qt.white, Qt.red, Qt.blue, Qt.yellow]
		names = ["black", "white", "red", "blue", "yellow"]

		colorMenu = QMenu(self)
		for color, name in zip(colors, names):
			action = QAction(Utils.createColorIcon(color), name, self,
					triggered=slot)
			action.setData(QColor(color))
			colorMenu.addAction(action)
			if color == defaultColor:
				colorMenu.setDefaultAction(action)
		return colorMenu

	def documentWasModified(self):
		self.setWindowModified(self.paged_text_edit.document().isModified())

	def about_pablo(self):
		QMessageBox.about(self, "About Pablo",
				"<b>Pablo</b> is a collaborative platform for writers."
				"<br>It includes a nice text editor, and the Pablo Collaboration Tool."
				"<br><br>Developed by Chukwuemeka Nwagu. ")

	@Slot(tuple)
	def readPageInfo(self, pageInfo):
		self.curPage = pageInfo
		pageMessage = str(pageInfo[0]) + " / " + str(pageInfo[1]) + "    "
		self.pageInfoStatusLabel.setText(pageMessage)

	def printMessageOnStatus(self, message, timeout=5000):                                                   
		self.statusBar.showMessage(message, timeout)

	def toggleNavigationBar(self):
		self.nav_bar.setVisible(not self.nav_bar.isVisible())

	def setTheme(self, themePath):
		self.container.setStyleSheet(".QWidget { border-image: url(" + themePath + ");}");

		# Get the dominant colour from the theme image
		NUM_CLUSTERS = 5
		im = Image.open(themePath)
		im = im.resize((150, 150))  # optional, to reduce time
		ar = np.asarray(im)
		shape = ar.shape
		ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

		codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)

		vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
		counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

		index_max = scipy.argmax(counts)                    # find most frequent
		peak = codes[index_max]
		colour_hex = '#%02x%02x%02x' % tuple(int(i) for i in peak)

		self.setStyleSheet("QMainWindow { background-color: " + colour_hex + " }");
		self.main_tool_bar.setStyleSheet(".QToolBar { background-color: transparent; border: none; } .QToolButton { margin-bottom: 10px; margin-top: 10px; } ")
		self.pageInfoStatusLabel.setStyleSheet(".QLabel { color: white; font-weight: 800; }")
		self.statusBar.setStyleSheet(".QStatusBar { background-color: transparent; border: none; color: white;}")
		self.nav_bar.setStyleSheet("QScrollArea { background-color: " + colour_hex + "; border: none; border-left: 1px solid white;}");


if __name__ == '__main__':

	import sys

	app = QApplication(sys.argv)
	pixmap = QPixmap("images/splash.png")
	splash = QSplashScreen(pixmap)
	splash.show()
	app.processEvents()

	main_win = create_main_window()
	exit_code = app.exec_()
	sys.exit(exit_code)
