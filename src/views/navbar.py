
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QSizePolicy

class NavBar(QScrollArea):

	CURRENT_TAB = 0
	
	def __init__(self):
		super(NavBar, self).__init__()
		
		self.setFixedWidth(200)
		sizePolicy = QSizePolicy()
		sizePolicy.setVerticalPolicy(QSizePolicy.Expanding)
		sizePolicy.setHorizontalPolicy(QSizePolicy.Maximum)
		self.setSizePolicy(sizePolicy)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		self.wid = QWidget()
		self.wid.setStyleSheet(".QWidget {background-color: transparent; border: none;}")
		self.vLayout = QVBoxLayout(self.wid)
		self.vLayout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
		self.vLayout.setMargin(0)
		self.setWidgetResizable(True)
		self.setWidget(self.wid)
		self.wid.setLayout(self.vLayout)
		
	def addComponent(self, component):
		self.vLayout.addWidget(component)
		component.setObjectName("barComp")
		component.setStyleSheet("QWidget#barComp { margin-bottom: 20px; margin-top: 20px }")

	def clearNavBar(self):
		while(self.vLayout.count() != 0):
			self.vLayout.takeAt(0).widget().setParent(None)
            