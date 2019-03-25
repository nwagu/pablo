
from PySide2.QtWidgets import QMenuBar, QAction
from PySide2.QtGui import QIcon, QKeySequence

from utils.genutils import GenUtils

class MenuBar(QMenuBar):
	
	def __init__(self, parent=None):
		super(MenuBar, self).__init__()

		self.parent = parent

		
		self.setObjectName("MyMenuBar")

		self.createActions()
		self.createMenus()
		

	def createMenus(self):
		self.file_menu = self.addMenu("&File")
		self.edit_menu = self.addMenu("&Edit")
		self.themes_menu = self.addMenu("&Themes")
		self.about_menu = self.addMenu("&About")

		self.file_menu.addAction(self.parent.new_action)
		self.file_menu.addAction(self.parent.open_action)
		self.file_menu.addAction(self.parent.save_action)
		self.file_menu.addAction(self.parent.save_as_action)
		self.file_menu.addSeparator()
		self.file_menu.addAction(self.parent.print_action)
		self.file_menu.addSeparator()
		self.file_menu.addAction(self.parent.exit_action)

		self.edit_menu.addAction(self.parent.cut_action)
		self.edit_menu.addAction(self.parent.copy_action)
		self.edit_menu.addAction(self.parent.paste_action)
		self.edit_menu.addSeparator()
		self.edit_menu.addAction(self.parent.undo_action)
		self.edit_menu.addAction(self.parent.redo_action)
		self.edit_menu.addSeparator()
		self.edit_menu.addAction(self.parent.select_all_action)
		self.edit_menu.addSeparator()
		self.edit_menu.addAction(self.parent.find_action)
		self.edit_menu.addSeparator()
		self.edit_menu.addAction(self.parent.word_count_action)
		self.edit_menu.addSeparator()
		self.edit_menu.addAction(self.parent.image_action)
		
		self.themes_menu.addAction(self.parent.themes_action)
		self.about_menu.addAction(self.parent.about_action)
		

	def createActions(self):
		self.parent.new_action  = QAction(QIcon(GenUtils.resource_path('src/images/new.png')), "&New", self.parent, shortcut=QKeySequence.New, statusTip="Create a New File", triggered=self.parent.newFile)
		self.parent.open_action = QAction(QIcon(GenUtils.resource_path('src/images/open.png')), "O&pen", self.parent, shortcut=QKeySequence.Open, statusTip="Open an existing file", triggered=self.parent.open)
		self.parent.save_action = QAction(QIcon(GenUtils.resource_path('src/images/save.png')), "&Save", self.parent, shortcut=QKeySequence.Save, statusTip="Save the current file to disk", triggered=self.parent.save)
		self.parent.save_as_action = QAction(QIcon(GenUtils.resource_path('src/images/save.png')), "Save &As...", self.parent, shortcut=QKeySequence.SaveAs, statusTip="Save the current file under a new name", triggered=self.parent.saveAs)
		self.parent.print_action = QAction(QIcon(GenUtils.resource_path('src/images/print.png')), "&Print...", self.parent, shortcut=QKeySequence.Print, statusTip="Print the current file", triggered=self.parent.print_)
		self.parent.exit_action = QAction(QIcon.fromTheme("application-exit"), "E&xit", self.parent, shortcut="Ctrl+Q", statusTip="Exit the Application", triggered=self.close)
		self.parent.cut_action = QAction(QIcon(GenUtils.resource_path('src/images/cut.png')), "C&ut", self.parent, shortcut=QKeySequence.Cut, statusTip="Cut the current selection to clipboard", triggered=self.parent.paged_text_edit.cut)
		self.parent.copy_action = QAction(QIcon(GenUtils.resource_path('src/images/copy.png')), "C&opy", self.parent, shortcut=QKeySequence.Copy, statusTip="Copy the current selection to clipboard", triggered=self.parent.paged_text_edit.copy)
		self.parent.paste_action = QAction(QIcon(GenUtils.resource_path('src/images/paste.png')), "&Paste", self.parent, shortcut=QKeySequence.Paste, statusTip="Paste the clipboard's content in current location", triggered=self.parent.paged_text_edit.paste)
		self.parent.select_all_action = QAction(QIcon(GenUtils.resource_path('src/images/selectAll.png')), "Select All", self.parent, statusTip="Select All", triggered=self.parent.paged_text_edit.selectAll)
		self.parent.redo_action = QAction(QIcon(GenUtils.resource_path('src/images/redo.png')),"Redo", self.parent, shortcut=QKeySequence.Redo, statusTip="Redo previous action", triggered=self.parent.paged_text_edit.redo)
		self.parent.undo_action = QAction(QIcon(GenUtils.resource_path('src/images/undo.png')),"Undo", self.parent, shortcut=QKeySequence.Undo, statusTip="Undo previous action", triggered=self.parent.paged_text_edit.undo)
		self.parent.themes_action = QAction(QIcon(GenUtils.resource_path('src/images/save.png')), "&Themes...", self.parent, statusTip = "Themes", triggered = self.parent.fontChange)
		self.parent.about_action = QAction(QIcon(GenUtils.resource_path('src/images/about.png')), 'A&bout', self.parent, shortcut = QKeySequence(QKeySequence.HelpContents), triggered=self.parent.about_pablo)
		self.parent.find_action = QAction(QIcon(GenUtils.resource_path('src/images/save.png')), '&Find', self.parent, shortcut = QKeySequence(QKeySequence.Find), triggered=self.parent._find)
		self.parent.word_count_action = QAction(QIcon(GenUtils.resource_path('src/images/save.png')), 'Word Count', self.parent, shortcut = "Ctrl+W", triggered=self.parent.showWordCount)
		self.parent.image_action = QAction(QIcon(GenUtils.resource_path('src/images/save.png')), 'I&mage', self.parent, shortcut = "Ctrl+Shift+I", statusTip = "Insert image", triggered=self.parent.insertImage)
		
		self.parent.cut_action.setEnabled(False)
		self.parent.copy_action.setEnabled(False)
		self.parent.undo_action.setEnabled(False)
		self.parent.redo_action.setEnabled(False)
		self.parent.paged_text_edit.copyAvailable.connect(self.parent.cut_action.setEnabled)
		self.parent.paged_text_edit.copyAvailable.connect(self.parent.copy_action.setEnabled)
		self.parent.paged_text_edit.undoAvailable.connect(self.parent.undo_action.setEnabled)
		self.parent.paged_text_edit.redoAvailable.connect(self.parent.redo_action.setEnabled)

