
from PySide2.QtWidgets import QWidget, QLabel, QDialog, QGridLayout
from utils.genutils import GenUtils

import re

class WordCount(QDialog):
    def __init__(self,parent = None):
        QDialog.__init__(self, parent)

        self.parent = parent

        self.initUI()

    def initUI(self):

        # Word count in selection
        currentLabel = QLabel("Current selection",self)
        currentLabel.setStyleSheet("font-weight:bold; font-size: 15px;")

        currentWordsLabel = QLabel("Words: ", self)
        currentSymbolsLabel = QLabel("Symbols: ",self)

        self.currentWords = QLabel(self)
        self.currentSymbols = QLabel(self)

        # Total word/symbol count
        totalLabel = QLabel("Total",self)
        totalLabel.setStyleSheet("font-weight:bold; font-size: 15px;")

        totalWordsLabel = QLabel("Words: ", self)
        totalSymbolsLabel = QLabel("Symbols: ",self)

        self.totalWords = QLabel(self)
        self.totalSymbols = QLabel(self)

        # Layout

        layout = QGridLayout(self)

        layout.addWidget(currentLabel,0,0)

        layout.addWidget(currentWordsLabel,1,0)
        layout.addWidget(self.currentWords,1,1)

        layout.addWidget(currentSymbolsLabel,2,0)
        layout.addWidget(self.currentSymbols,2,1)

        spacer = QWidget()
        spacer.setFixedSize(0,5)

        layout.addWidget(spacer,3,0)

        layout.addWidget(totalLabel,4,0)

        layout.addWidget(totalWordsLabel,5,0)
        layout.addWidget(self.totalWords,5,1)

        layout.addWidget(totalSymbolsLabel,6,0)
        layout.addWidget(self.totalSymbols,6,1)

        self.setWindowTitle("Word count")
        self.setGeometry(300,300,200,200)
        self.setLayout(layout)

    def getText(self):

        # Get the text currently in selection
        text = self.parent.paged_text_edit.textCursor().selectedText()
        count = GenUtils.count_words(text)
        self.currentWords.setText(count[0])
        self.currentSymbols.setText(count[1])

        # For the total count...
        text = self.parent.paged_text_edit.toPlainText()
        count = GenUtils.count_words(text)
        self.totalWords.setText(count[0])
        self.totalSymbols.setText(count[1])