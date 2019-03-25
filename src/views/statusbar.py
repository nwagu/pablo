

from PySide2.QtWidgets import QStatusBar

from views.clickablelabel import ClickableLabel

class StatusBar(QStatusBar):
	
	def __init__(self, parent=None):
		super(StatusBar, self).__init__()

		self.parent = parent

		self.setObjectName("MyStatusBar")
		self.setStyleSheet("QStatusBar#MyStatusBar { background-color: transparent; border: none; color: white;}")

		self.createLabels()
		

	def createLabels(self):
		self.wordCountLabel = ClickableLabel()
		self.wordCountLabel.clicked.connect(self.parent.word_count_action.triggered.emit)
		self.addPermanentWidget(self.wordCountLabel)
		
		self.pageInfoStatusLabel = ClickableLabel()
		# self.pageInfoStatusLabel.clicked.connect(TODO)
		self.addPermanentWidget(self.pageInfoStatusLabel)
	
	def writeMessageOnStatus(self, message, timeout=5000):                                                   
		self.showMessage(message, timeout)

	def writeWordCount(self, message):
		self.wordCountLabel.setText(message)

	def writePageInfo(self, message):
		self.pageInfoStatusLabel.setText(message)
