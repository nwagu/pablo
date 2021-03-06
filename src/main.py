
import sys

import time

from PBL.htmlcleaner import HTMLCleaner
from views import pagedtextedit, navpanel, dropview, menubar, toolbar, statusbar
from ext import find, wordcount
from utils.colorutils import ColorUtils
from utils.genutils import GenUtils

from PySide2.QtCore import Qt, QMarginsF, Slot, QSettings, QPoint, QSize, QFile, QFileInfo, QTextStream
from PySide2.QtGui import QPageSize, QPixmap, QTextCharFormat, QTextDocument, QIcon, QFont
from PySide2.QtWidgets import QApplication, QMainWindow, QFrame, QHBoxLayout, QDialog, QProgressBar
from PySide2.QtWidgets import QFileDialog, QMessageBox, QSplashScreen
from PySide2.QtPrintSupport import QPrintDialog, QPrinter
from PIL import Image

main_windows = []
m_theme = GenUtils.resource_path('src/themes/13.jpg')

def create_main_window(): # TODO this function should require a theme attribute
	"""Creates a MainWindow."""
	main_win = MainWindow()
	main_win.setTheme(m_theme)
	main_windows.append(main_win)
	main_win.show()
	return main_win
		

class MainWindow(QMainWindow):
	"""Contains a menubar, statusbar
	also contains a QStackedWidget DropView as central widget.
	dropView contains the PagedTextEdit. """
	def __init__(self, fileName=None):
		super(MainWindow, self).__init__()

		self.curFile = ''
		self.curPage = (0, 0) # Tuple containing current page and total pages of the current file

		self.setWindowTitle('Pablo Editor')
		self.setWindowIcon(QIcon(GenUtils.resource_path('src/images/icon.ico')))
		self.setWindowState(Qt.WindowFullScreen)
		self.setWindowState(Qt.WindowMaximized)
		# available_geometry = app.desktop().availableGeometry(self)
		# self.resize(available_geometry.width(), available_geometry.height())
		self.readSettings()

		self.dropView = dropview.DropView()

		self.paged_text_edit = pagedtextedit.PagedTextEdit(self.dropView)
		# The textedit must be transparent; the white pages are painted in paintEvent() function
		self.paged_text_edit.setStyleSheet("QTextEdit { background-color: transparent }")

		self.paged_text_edit.setFrameStyle(QFrame.NoFrame) # Removes a border-like line around the TextEdit

		doc = QTextDocument()
		font = QFont()
		font.setPointSize(12)
		font.setFamily('Calibri')
		doc.setDefaultFont(font)
		# doc.setDefaultStyleSheet("body { font-color: black; font-family: Calibri; font-size: 12;} ")
		self.paged_text_edit.setDocument(doc)
		self.paged_text_edit.setPageFormat(QPageSize.A5Extra)
		self.paged_text_edit.setPageMargins(QMarginsF(15, 15, 15, 15))
		self.paged_text_edit.setUsePageMode(True)
		self.paged_text_edit.setPageNumbersAlignment(Qt.AlignBottom | Qt.AlignCenter)

		self.text_edit_layout = QHBoxLayout()
		self.text_edit_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		
		self.text_edit_layout.setMargin(0)
		self.paged_text_edit.setLayout(self.text_edit_layout)

		# This below block of code prevents undoing the setDocumentMargin() and setFrameformat()
		# methods in the aboutUpdateDocumentGeometry function
		self.paged_text_edit.aboutUpdateDocumentGeometry()
		# self.paged_text_edit.document().clearUndoRedoStack() # this does not work
		# These commands work
		self.paged_text_edit.document().setUndoRedoEnabled(False)
		self.paged_text_edit.document().setUndoRedoEnabled(True)

		self.setCentralWidget(self.dropView)

		self.dropView.addWidget(self.paged_text_edit)
		self.dropView.setCurrentWidget(self.paged_text_edit)

		self._setup_components()

		self.setCurrentFile('')
		self.paged_text_edit.document().contentsChanged.connect(self.documentWasModified)
		self.paged_text_edit.currentCharFormatChanged.connect(self.updateFontWidgets)
		self.paged_text_edit.cursorPositionChanged.connect(self.updatePositions)
		self.paged_text_edit.pageInfo.connect(self.readPageInfo)
		
		self.statusBar.writeMessageOnStatus("Ready", 10000)

	def _setup_components(self):

		self.toolBar = toolbar.ToolBar(self)
		self.addToolBar(Qt.LeftToolBarArea, self.toolBar)

		self.menuBar = menubar.MenuBar(self)
		self.setMenuBar(self.menuBar)

		self.statusBar = statusbar.StatusBar(self)
		self.setStatusBar(self.statusBar)

		self.nav_panel = navpanel.NavPanel(self)
		self.nav_panel.setVisible(False)
		self.text_edit_layout.addWidget(self.nav_panel)

	def navSelectorClicked(self, page):
		self.nav_panel.setCurrentPage(page)

	def newFile(self):
		if self.maybeSave():
			self.paged_text_edit.clear()
			self.setCurrentFile('')

	def open(self):
		fileName, filtr = QFileDialog.getOpenFileName(self, "Open File", 
				GenUtils.resource_path('src/files'), "PBL Files (*.pbl *.html)")
		if fileName:
			if self.maybeSave():
				self.loadFile(fileName)

	def save(self):
		if self.curFile:
			return self.saveFile(self.curFile)

		return self.saveAs()

	def saveAs(self):
		fileName, filtr = QFileDialog.getSaveFileName(self, "Save File", 
				GenUtils.resource_path("src/files"), "PBL Files (*.pbl)")
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

		if (QFileInfo(fileName).suffix() in ("pbl")):
			self.paged_text_edit.setHtml(inFile.readAll())
		elif (QFileInfo(fileName).suffix() in ("html")):
			# FIXME: Prevent double setting of the paged_text_edit where necessary
			# FIXME: Double setting may cause bad UX with large files
			self.paged_text_edit.setHtml(inFile.readAll())
			cleanHtml = HTMLCleaner.clean(self.paged_text_edit.toHtml()).decode("utf-8")
			self.paged_text_edit.setHtml(cleanHtml)
		else:
			self.paged_text_edit.setPlainText(inFile.readAll())

		QApplication.restoreOverrideCursor()

		self.setCurrentFile(fileName)
		self.statusBar.writeMessageOnStatus("File loaded", 2000)

	def saveFile(self, fileName):
		file = QFile(fileName)
		if not file.open(QFile.WriteOnly | QFile.Text):
			QMessageBox.warning(self, "Pablo",
					"Cannot write file %s:\n%s." % (fileName, file.errorString()))
			return False

		outFile = QTextStream(file)
		QApplication.setOverrideCursor(Qt.WaitCursor)

		if (QFileInfo(fileName).suffix() in ("pbl", "html")):
			# outFile << self.paged_text_edit.toHtml()
			outFile << HTMLCleaner.clean(self.paged_text_edit.toHtml())
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

		self.statusBar.writeMessageOnStatus("Ready", 2000)

	def strippedName(self, fullFileName):
		return QFileInfo(fullFileName).fileName()
	
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
		
	def _bold(self):
		# format = QTextCharFormat()
		# format.setFontWeight(QFont.Bold if self.edit_actions[0].isChecked() else QFont.Normal)
		# self.paged_text_edit.mergeCurrentCharFormat(format)
 
		if self.paged_text_edit.fontWeight() == QFont.Bold:
			self.paged_text_edit.setFontWeight(QFont.Normal)
		else:
			self.paged_text_edit.setFontWeight(QFont.Bold)
		
	def _italic(self):
		# format = QTextCharFormat()
		# format.setFontItalic(self.edit_actions[1].isChecked())
		# self.paged_text_edit.mergeCurrentCharFormat(format)

		state = self.paged_text_edit.fontItalic()
		self.paged_text_edit.setFontItalic(not state)
		
	def _underline(self):
		# format = QTextCharFormat()
		# format.setFontUnderline(self.edit_actions[2].isChecked())
		# self.paged_text_edit.mergeCurrentCharFormat(format)

		state = self.paged_text_edit.fontUnderline()
		self.paged_text_edit.setFontUnderline(not state)

	def _strike(self):
		format = self.paged_text_edit.currentCharFormat()
		format.setFontStrikeOut(not format.fontStrikeOut())
		self.paged_text_edit.setCurrentCharFormat(format)
	
	def _superscript(self):
		format = self.paged_text_edit.currentCharFormat()
		align = format.verticalAlignment()
		if(align == QTextCharFormat.AlignNormal):
			format.setVerticalAlignment(QTextCharFormat.AlignSuperScript)
		else:
			format.setVerticalAlignment(QTextCharFormat.AlignNormal)
		self.paged_text_edit.setCurrentCharFormat(format)
	
	def _subscript(self):
		format = self.paged_text_edit.currentCharFormat()
		align = format.verticalAlignment()
		if(align == QTextCharFormat.AlignNormal):
			format.setVerticalAlignment(QTextCharFormat.AlignSubScript)
		else:
			format.setVerticalAlignment(QTextCharFormat.AlignNormal)
		self.paged_text_edit.setCurrentCharFormat(format)
		
	def _fontFamily(self, font):
		self.paged_text_edit.setFontFamily(font.family())

	def _fontSize(self, size):
		self.paged_text_edit.setFontPointSize(int(size))

	def _fontColor(self, color):
		self.paged_text_edit.setTextColor(color)

	def pageScaleChanged(self, scale):
		self.paged_text_edit.setPageFormat(GenUtils.getPageFormatFromString(scale))

	def _indent(self, alignment):
		
		if(alignment != Qt.AlignLeft):
			# If applied indent is already present, revert to default left indent
			if(self.paged_text_edit.alignment() == alignment):
				self.paged_text_edit.setAlignment(Qt.AlignLeft)
			else:
				self.paged_text_edit.setAlignment(alignment)
		else:
				self.paged_text_edit.setAlignment(alignment)

		self.nav_panel.updateIndentWidgets(alignment)

	def _list(self, listType):
		cursor = self.paged_text_edit.textCursor()
		if(cursor.currentList()):
			cursor.insertList(listType)
		else:
			cursor.createList(listType)
		
	@Slot(QTextCharFormat)
	def updateFontWidgets(self, format):
		self.nav_panel.updateFormatWidgets(format)

	def updatePositions(self):
		self.updateCursorPosition()
		self.nav_panel.updateIndentWidgets(self.paged_text_edit.alignment())
		# list = self.paged_text_edit.textCursor().currentList()
		# if(list):
		# 	self.nav_panel.updateListWidgets(list.format())

	def _find(self):
		ff = find.Find(self)
		ff.show()

	def insertImage(self):
		# Get image file name
		filename = QFileDialog.getOpenFileName(self, 
					'Insert image',".","Images (*.png *.xpm *.jpg *.bmp *.gif)")[0]

		# Create image object
		image = QImage(filename)

		# Error if unloadable
		if image.isNull():

			popup = QMessageBox(QMessageBox.Critical,"Image load error",
									"Could not load image file!",QMessageBox.Ok, self)
			popup.show()

		else:

			cursor = self.paged_text_edit.textCursor()
			cursor.insertImage(image, filename)

	def showWordCount(self):
		wc = wordcount.WordCount(self)
		wc.getText()
		wc.show()

	def documentWasModified(self):
		self.setWindowModified(self.paged_text_edit.document().isModified())
		self.updateWordCount()

	def about_pablo(self):
		QMessageBox.about(self, "About Pablo",
				"<b>Pablo</b> is a collaborative platform for writers."
				"<br>It includes a nice text editor, and the Pablo Collaboration Tool."
				"<br><br>Developed by Chukwuemeka Nwagu. ")

	@Slot(tuple)
	def readPageInfo(self, pageInfo):
		self.curPage = pageInfo
		pageMessage = "  " + str(pageInfo[0]) + " / " + str(pageInfo[1]) + "    "
		self.statusBar.writePageInfo(pageMessage)

	def updateWordCount(self):
		count = GenUtils.count_words(self.paged_text_edit.toPlainText())
		# Generate string and add 's' when quantity is more than one
		wordCountInfo = "{} {}, {} {}   ".format(count[0], "words" if count[0] > 1 else "word", count[1], "symbols" if count[1] > 1 else "symbol")
		self.statusBar.writeWordCount(wordCountInfo)

	def updateCursorPosition(self):
		cursor = self.paged_text_edit.textCursor()
		line = cursor.blockNumber() + 1 # index to start from 1
		col = cursor.columnNumber() + 1 # index to start from 1
		self.statusBar.writeCursorPosition("Ln: {}, Col: {}   ".format(line, col))

	def setTheme(self, themePath):
		# Get theme color from theme image
		mainColorHex = ColorUtils.getDominantColorFromImage(Image.open(themePath))

		# Set image as main background
		self.dropView.dropImage(themePath)
		self.setStyleSheet("QMainWindow { background-color: " + mainColorHex + " }")

		# Set theme color on other views in the application appropriately
		self.nav_panel.setThemeColor(mainColorHex)
		self.paged_text_edit.setThemeColor(mainColorHex)


if __name__ == '__main__':

	app = QApplication(sys.argv)
	pixmap = QPixmap(GenUtils.resource_path("src/images/splash.jpg"))
	splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)

	progressBar = QProgressBar(splash)
	progressBar.setFixedSize(splash.width(), 5)
	progressBar.setTextVisible(False)
	progressBar.setStyleSheet(" QProgressBar { background-color: red; } QProgressBar::chunk { background-color: orange }")
	splash.setMask(pixmap.mask())

	splash.show()
	for i in range(0, 100):
		progressBar.setValue(i)
		t = time.time()
		while time.time() < t + 0.01:
			app.processEvents()

	app.processEvents()

	main_win = create_main_window()
	splash.finish(main_win)
	exit_code = app.exec_()
	sys.exit(exit_code)
