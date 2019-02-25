import sys

import struct
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
from pagedtextedit import PagedTextEdit
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PIL import Image

main_windows = []
m_theme = "themes/7.jpg"

def create_main_window(): # TODO this function should require a theme attribute
    """Creates a MainWindow."""
    main_win = MainWindow()
    main_win._setup_components()
    main_win.setTheme(m_theme)
    main_windows.append(main_win)
    main_win.show()
    return main_win

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

        self.paged_text_edit = PagedTextEdit()
        # The textedit must be transparent; the white pages are painted in paintEvent() function
        self.paged_text_edit.setStyleSheet("QTextEdit { background-color: rgb(255, 255, 255, 0) }")

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
        # self.filters = "Text files (*.txt)"
        self.paged_text_edit.document().contentsChanged.connect(self.documentWasModified)
        


    def _setup_components(self):
        self._create_menus()
        self._create_actions()
        # self._create_tool_bar()
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.printMessageOnStatus("Ready", 10000)
        self.paged_text_edit.pageInfo.connect(self.readPageInfo)

        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
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

        # self.main_tool_bar.addAction(self.new_action)
        # self.main_tool_bar.addAction(self.open_action)
        # self.main_tool_bar.addAction(self.save_action)
        # self.main_tool_bar.addSeparator()
        # self.main_tool_bar.addAction(self.cut_action)
        # self.main_tool_bar.addAction(self.copy_action)
        # self.main_tool_bar.addAction(self.paste_action)
        # self.main_tool_bar.addSeparator()
        # self.main_tool_bar.addAction(self.undo_action)
        # self.main_tool_bar.addAction(self.redo_action)

    def _create_actions(self):
        self.new_action  = QAction(QIcon('images/new.png'), "&New", self, shortcut=QKeySequence.New, 
                        statusTip="Create a New File", triggered=self.newFile)
        self.open_action = QAction(QIcon('images/open.png'), "O&pen", self, shortcut=QKeySequence.Open, 
                        statusTip="Open an existing file", triggered=self.open)
        self.save_action = QAction(QIcon('images/save.png'), "&Save", self, shortcut=QKeySequence.Save, 
                        statusTip="Save the current file to disk", triggered=self.save)
        self.save_as_action = QAction(QIcon('images/save.png'), "Save &As...", self, shortcut=QKeySequence.SaveAs, 
                        statusTip="Save the current file under a new name", triggered=self.saveAs)
        self.exit_action = QAction(QIcon.fromTheme("application-exit"), "E&xit", self, shortcut="Ctrl+Q", 
                        statusTip="Exit the Application", triggered=self.close)
        self.cut_action = QAction(QIcon('images/cut.png'), "C&ut", self, shortcut=QKeySequence.Cut, statusTip="Cut the current selection to clipboard", triggered=self.paged_text_edit.cut)
        self.copy_action = QAction(QIcon('images/copy.png'), "C&opy", self, shortcut=QKeySequence.Copy, statusTip="Copy the current selection to clipboard", triggered=self.paged_text_edit.copy)
        self.paste_action = QAction(QIcon('images/paste.png'), "&Paste", self, shortcut=QKeySequence.Paste, statusTip="Paste the clipboard's content in current location", triggered=self.paged_text_edit.paste)
        self.select_all_action = QAction(QIcon('images/selectAll.png'), "Select All", self, statusTip="Select All", triggered=self.paged_text_edit.selectAll)
        self.redo_action = QAction(QIcon('images/redo.png'),"Redo", self, shortcut=QKeySequence.Redo, statusTip="Redo previous action", triggered=self.paged_text_edit.redo)
        self.undo_action = QAction(QIcon('images/undo.png'),"Undo", self, shortcut=QKeySequence.Undo, statusTip="Undo previous action", triggered=self.paged_text_edit.undo)
        self.themes_action = QAction(QIcon('images/save.png'), "&Themes...", self, statusTip = "Themes", triggered = self.fontChange)
        self.font_action = QAction("F&ont", self, statusTip = "Modify font properties", triggered = self.fontChange)
        self.about_action = QAction(QIcon('images/about.png'), 'A&bout', self,
                                shortcut = QKeySequence(QKeySequence.HelpContents), triggered=self.about_pablo)

        self.cut_action.setEnabled(False)
        self.copy_action.setEnabled(False)
        self.paged_text_edit.copyAvailable.connect(self.cut_action.setEnabled)
        self.paged_text_edit.copyAvailable.connect(self.copy_action.setEnabled)

    def _create_tool_bar(self):
        self.main_tool_bar = self.addToolBar('Main')
        self.main_tool_bar.setMovable(False)
        self.main_tool_bar.setStyleSheet("QToolBar { background: rgb(0, 0, 0, 0); border: none;}")

    def _create_menus(self):
        self.file_menu = self.menuBar().addMenu("&File")
        self.edit_menu = self.menuBar().addMenu("&Edit")
        self.themes_menu = self.menuBar().addMenu("&Themes")
        self.about_menu = self.menuBar().addMenu("&About")

    def newFile(self):
        if self.maybeSave():
            self.paged_text_edit.clear()
            self.setCurrentFile('')

    def open(self):
        if self.maybeSave():
            fileName, filtr = QFileDialog.getOpenFileName(self)
            if fileName:
                self.loadFile(fileName)

    def save(self):
        if self.curFile:
            return self.saveFile(self.curFile)

        return self.saveAs()

    def saveAs(self):
        fileName, filtr = QFileDialog.getSaveFileName(self)
        if fileName:
            return self.saveFile(fileName)

        return False

    def loadFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "Pablo",
                    "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return

        inf = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.paged_text_edit.setPlainText(inf.readAll())
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.printMessageOnStatus("File loaded", 2000)

    def saveFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Pablo",
                    "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return False

        outf = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)

        # FIXME: Once file is out of scope, the file is empty, instead of having text.
        outf << self.paged_text_edit.toPlainText()
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
        self.printMessageOnStatus("Page " + str(pageInfo[0]) + " of " + str(pageInfo[1]))

    def printMessageOnStatus(self, message, timeout=5000):                                                   
        self.statusBar.showMessage(message, timeout)

    def setTheme(self, themePath):
        self.container.setStyleSheet(".QWidget { border-image: url(" + themePath + ");}");
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
        self.statusBar.setStyleSheet("QStatusBar { background-color: " + colour_hex + "; border: none;}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pixmap = QPixmap("images/splash.png")
    splash = QSplashScreen(pixmap)
    # splash.show()
    app.processEvents()

    main_win = create_main_window()
    exit_code = app.exec_()
    sys.exit(exit_code)
