import sys

# from pabloview import PabloView
from pagedtextedit import PagedTextEdit
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

main_windows = []

def create_main_window():
    """Creates a MainWindow."""
    main_win = MainWindow()
    main_windows.append(main_win)
    main_win.show()
    return main_win

class MainWindow(QMainWindow):
    """Provides the parent window that includes the BookmarkWidget,
    BrowserTabWidget, and a DownloadWidget, to offer the complete
    web browsing experience."""
    def __init__(self, fileName=None):
        super(MainWindow, self).__init__()

        self.setWindowTitle('Pablo Editor')
        self.setWindowIcon(QIcon('images/icon.png'))

        self.paged_text_edit = PagedTextEdit()

        bkgnd = QPixmap("images/bkg1.jpg");
        bkgnd = bkgnd.scaled(self.size(), Qt.IgnoreAspectRatio);
        palette = QPalette()
        palette.setBrush(QPalette.Window, bkgnd)

        self.paged_text_edit.setPalette(palette)
        self.paged_text_edit.setAutoFillBackground(True)
        self.doc = QTextDocument()
        font = QFont()
        font.setPointSize(20)
        font.setFamily('Calibri')
        self.doc.setDefaultFont(font)
        self.paged_text_edit.setDocument(self.doc)
        self.paged_text_edit.setPageFormat(QPageSize.A5);
        self.paged_text_edit.setPageMargins(QMarginsF(15, 15, 15, 15));
        self.paged_text_edit.setUsePageMode(True);
        self.paged_text_edit.setAddSpaceToBottom(False) # not needed in paged mode
        self.paged_text_edit.setPageNumbersAlignment(Qt.AlignBottom | Qt.AlignRight);
        self.paged_text_edit.resize(400, 1000); # This does not work

        self.paged_text_edit.setText(open("files/chekhov.pbl").read())
        self.setWindowState(Qt.WindowFullScreen)
        self.setWindowState(Qt.WindowMaximized)
        self.setCentralWidget(self.paged_text_edit)

        # self.fileName = None
        # self.filters = "Text files (*.txt)"

    def _setup_components(self):
        self._create_menus()
        self._create_actions()
        self._create_tool_bar()
        self.myStatusBar = QStatusBar()
        self.setStatusBar(self.myStatusBar)
        self.myStatusBar.showMessage('Ready')
        # self.myStatusBar.showMessage('Ready', 10000)

        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)
        self.edit_menu.addAction(self.cut_action)
        self.edit_menu.addAction(self.copy_action)
        self.edit_menu.addAction(self.paste_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.undo_action)
        self.edit_menu.addAction(self.redo_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.select_all_action)

        self.window_menu.addAction(self.zoom_in_action)
        self.window_menu.addAction(self.zoom_out_action)
        self.window_menu.addAction(self.reset_zoom_action)
        self.about_menu.addAction(self.about_action)

        self.main_tool_bar.addAction(self.new_action)
        self.main_tool_bar.addAction(self.open_action)
        self.main_tool_bar.addAction(self.save_action)
        self.main_tool_bar.addSeparator()
        self.main_tool_bar.addAction(self.cut_action)
        self.main_tool_bar.addAction(self.copy_action)
        self.main_tool_bar.addAction(self.paste_action)
        self.main_tool_bar.addSeparator()
        self.main_tool_bar.addAction(self.undo_action)
        self.main_tool_bar.addAction(self.redo_action)

    def _create_actions(self):
        self.new_action  = QAction( QIcon('images/new.png'), '&New', self, shortcut=QKeySequence.New, 
                        statusTip="Create a New File", triggered=self.newFile)
        self.open_action = QAction( QIcon('images/open.png'), 'O&pen', self, shortcut=QKeySequence.Open, 
                        statusTip="Open an existing file", triggered=self.openFile)
        self.save_action = QAction( QIcon('images/save.png'), '&Save', self, shortcut=QKeySequence.Save, 
                        statusTip="Save the current file to disk", triggered=self.saveFile)
        self.exit_action = QAction(QIcon.fromTheme("application-exit"), 'E&xit', self, shortcut="Ctrl+Q", 
                        statusTip="Exit the Application", triggered=qApp.quit)
        self.cut_action = QAction(QIcon('images/cut.png'), 'C&ut', self, shortcut=QKeySequence.Cut, statusTip="Cut the current selection to clipboard", triggered=self.saveFile)
        self.copy_action = QAction(QIcon('images/copy.png'), 'C&opy', self, shortcut=QKeySequence.Copy, statusTip="Copy the current selection to clipboard", triggered=self.saveFile)
        self.paste_action = QAction(QIcon('images/paste.png'), '&Paste', self, shortcut=QKeySequence.Paste, statusTip="Paste the clipboard's content in current location", triggered=self.saveFile)
        self.select_all_action = QAction(QIcon('images/selectAll.png'), 'Select All', self, statusTip="Select All", triggered=self.saveFile)
        self.redo_action = QAction(QIcon('images/redo.png'),'Redo', self, shortcut=QKeySequence.Redo, statusTip="Redo previous action", triggered=self.saveFile)
        self.undo_action = QAction(QIcon('images/undo.png'),'Undo', self, shortcut=QKeySequence.Undo, statusTip="Undo previous action", triggered=self.saveFile)
        self.zoom_in_action = QAction(QIcon.fromTheme("zoom-in"), "Zoom In", self,
                               shortcut = QKeySequence(QKeySequence.ZoomIn), triggered = self._zoom_in)
        self.zoom_out_action = QAction(QIcon.fromTheme("zoom-out"), "Zoom Out", self,
                                shortcut = QKeySequence(QKeySequence.ZoomOut), triggered = self._zoom_out)
        self.reset_zoom_action = QAction(QIcon.fromTheme("zoom-original"), "Reset Zoom", self,
                                shortcut = "Ctrl+0", triggered = self._reset_zoom)
        self.font_action = QAction('F&ont', self, statusTip = "Modify font properties", triggered = self.fontChange)
        self.about_action = QAction(QIcon('images/about.png'), 'A&bout', self,
                                shortcut = QKeySequence(QKeySequence.HelpContents), triggered=self.about_pablo)

    def _create_tool_bar(self):
        self.main_tool_bar = self.addToolBar('Main')
        self.main_tool_bar.setMovable(False)

    def _create_menus(self):
        self.file_menu = self.menuBar().addMenu("&File")
        self.edit_menu = self.menuBar().addMenu("&Edit")
        self.window_menu = self.menuBar().addMenu("&Window")
        self.about_menu = self.menuBar().addMenu("&About")

    def newFile(self):
        if self.maybeSave():
            self.textEdit.clear()
            self.setCurrentFile('')

    def openFile(self):
        if self.maybeSave():
            fileName, filtr = QtWidgets.QFileDialog.getOpenFileName(self)
            if fileName:
                self.loadFile(fileName)

    def saveFile(self):
        if self.curFile:
            return self.saveFile(self.curFile)

        return self.saveAs()

    def saveAs(self):
        fileName, filtr = QtWidgets.QFileDialog.getSaveFileName(self)
        if fileName:
            return self.saveFile(fileName)

        return False

    def fontChange(self):
        (font, ok) = QFontDialog.getFont(QFont("Helvetica[Cronyx]", 10), self)
        if ok:
            self.textEdit.setCurrentFont(font)
    
    def _zoom_in(self):
        new_zoom = self._tab_widget.zoom_factor() * 1.5
        if (new_zoom <= WebEngineView.maximum_zoom_factor()):
            self._tab_widget.set_zoom_factor(new_zoom)
            self._update_zoom_label()

    def _zoom_out(self):
        new_zoom = self._tab_widget.zoom_factor() / 1.5
        if (new_zoom >= WebEngineView.minimum_zoom_factor()):
            self._tab_widget.set_zoom_factor(new_zoom)
            self._update_zoom_label()

    def _reset_zoom(self):
        self._tab_widget.set_zoom_factor(1)
        self._update_zoom_label()

    def _update_zoom_label(self):
        percent = int(self._tab_widget.zoom_factor() * 100)
        self._zoom_label.setText("{}%".format(percent))

    def about_pablo(self):
        QMessageBox.about(self, "About Pablo",
                "<b>Pablo</b> is a collaborative platform for writers."
                "<br>It includes a nice text editor, and the Pablo Collaboration Tool."
                "<br><br>Developed by Chukwuemeka Nwagu. ")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pixmap = QPixmap("images/splash.png")
    splash = QSplashScreen(pixmap)
    splash.show()
    app.processEvents()

    main_win = create_main_window()
    main_win._setup_components()
    #initial_files is used if user is opening the app by double-clicking a .pabl file
    initial_files = sys.argv[1:]
    if not initial_files:
        initial_files.append('c:/')
    for file in initial_files:
        # main_win.load_file_in_new_tab(file)
        pass
    exit_code = app.exec_()
    sys.exit(exit_code)
