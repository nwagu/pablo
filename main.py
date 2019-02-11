import sys

from PySide2.QtWidgets import QDialog, QApplication, QWidget
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout
from PySide2.QtWidgets import QLineEdit, QLabel, QPushButton, QTextEdit
from PySide2.QtCore import Qt
from requests import Session


class MainActivity(QWidget):

	name = '' # Enter your name here!
	chat_url = 'https://build-system.fman.io/chat'
	server = Session()

	
	app = QApplication([])
 
	def __init__(self, parent=None):
		"""Constructor"""
		super(MainActivity, self).__init__(parent)
		
		main_layout = QVBoxLayout()
		
		text_area = QTextEdit()
		#text_area.returnPressed.connect(self.send_message)
		message = QLineEdit()
		message.setFocusPolicy(Qt.NoFocus)
		
		main_layout.addWidget(text_area)
		main_layout.addWidget(message)
		
		self.setLayout(main_layout)
		
		#self.app.exec_()
	

	# Event handlers:
	def display_new_messages():
		new_message = server.get(chat_url).text
		if new_message:
			text_area.append(new_message)

	def send_message():
		server.post(chat_url, {'name': name, 'message': message.text()})
		message.clear()

 
if __name__ == "__main__":
    ma = MainActivity()
    ma.show()
    sys.exit(ma.app.exec_())
