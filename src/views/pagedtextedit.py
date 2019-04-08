
from views.pagemetrics import PageMetrics
from PySide2.QtWidgets import QTextEdit
from PySide2.QtGui import QPainter, QPainterPath, QPen, QFont, QColor
from PySide2.QtCore import Qt, Slot, QSizeF, QMargins, QMarginsF, QRect, QRectF, Signal

class PagedTextEdit(QTextEdit):

	m_document = 0
	m_usePageMode = False
	m_addBottomSpace = True
	m_showPageNumbers  = True
	m_pageNumbersAlignment = Qt.AlignTop | Qt.AlignRight
	m_pageMetrics = PageMetrics()

	# Signals
	pageInfo = Signal(tuple)

	def __init__(self, *widget):
		super(PagedTextEdit, self).__init__()
		self.setAcceptRichText(True)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		
		# Configuring document change checking
		self.aboutDocumentChanged()
		# self.textChanged.connect(self.aboutDocumentChanged())

		# Manual adjustment of the scroll interval
		self.verticalScrollBar().rangeChanged.connect(self.aboutVerticalScrollRangeChanged)

	def goToPage(self, pageNumber):
		pageHeight = self.m_pageMetrics.pxPageSize().height()
		value = (pageNumber - 1) * pageHeight
		self.verticalScrollBar().setValue(value)

	def setPageFormat(self, _pageFormat):
		self.m_pageMetrics.update(_pageFormat, self.m_pageMetrics.m_mmPageMargins)
		
		# Redraw ourselves
		self.repaint()

	def setPageMargins(self, _margins):
		self.m_pageMetrics.update(self.m_pageMetrics.pageFormat(), _margins)

		# Redraw ourselves
		self.repaint()

	def usePageMode(self):
		return self.m_usePageMode

	def setUsePageMode(self, _use):
		if (self.m_usePageMode != _use):
			self.m_usePageMode = _use

			# Redraw ourselves
			self.repaint()

	def setAddSpaceToBottom(self, _addSpace):
		if (self.m_addBottomSpace != _addSpace):
			self.m_addBottomSpace = _addSpace

			# Redraw ourselves
			self.repaint()

	def setShowPageNumbers(self, _show):
		if (self.m_showPageNumbers != _show):
			self.m_showPageNumbers = _show
			# Redraw ourselves
			self.repaint()

	def setPageNumbersAlignment(self, _align):
		if (self.m_pageNumbersAlignment != _align):
			self.m_pageNumbersAlignment = _align

			# Redraw ourselves
			self.repaint()

	def paintEvent(self, _event):
		self.updateVerticalScrollRange()
		self.paintPagesView()
		self.paintPageNumbers()
		super().paintEvent(_event)

	def resizeEvent(self, _event):
		self.updateViewportMargins()
		self.updateVerticalScrollRange()
		super().resizeEvent(_event)

	def updateViewportMargins(self):
		# We form display parameters
		viewportMargins = QMargins()

		if (self.m_usePageMode):
			# Customize Document Size
			pageWidth = self.m_pageMetrics.pxPageSize().width()
			pageHeight = self.m_pageMetrics.pxPageSize().height()

			# Calculate indents for viewport
			DEFAULT_TOP_MARGIN = 5
			DEFAULT_BOTTOM_MARGIN = 0
			leftMargin = 0
			rightMargin = 0

			# If the width of the editor is greater than the width of the page of the document, expand the side margins.
			if (self.width() > pageWidth):
				VERTICAL_SCROLLBAR_WIDTH = self.verticalScrollBar().width() if self.verticalScrollBar().isVisible() else 0
				# ... the width of the viewport frame and the editor itself
				leftMargin = rightMargin = (self.width() - pageWidth - VERTICAL_SCROLLBAR_WIDTH) / 2
			

			topMargin = DEFAULT_TOP_MARGIN

			# The lower limit may be greater than the minimum value, for the case
			# when the whole document and even more fit on the screen
			bottomMargin = DEFAULT_BOTTOM_MARGIN
			documentHeight = pageHeight * self.document().pageCount()
			if ((self.height() - documentHeight) > (DEFAULT_TOP_MARGIN + DEFAULT_BOTTOM_MARGIN)):
				HORIZONTAL_SCROLLBAR_HEIGHT = self.horizontalScrollBar().height() if self.horizontalScrollBar().isVisible() else 0
				bottomMargin = self.height() - documentHeight - HORIZONTAL_SCROLLBAR_HEIGHT - DEFAULT_TOP_MARGIN

			# Adjust the indents themselves
			# rightMargin minus 200 to give space for user notes
			viewportMargins = QMargins(leftMargin, topMargin, rightMargin, bottomMargin)
		

		self.setViewportMargins(viewportMargins)

		self.aboutUpdateDocumentGeometry()

	def updateVerticalScrollRange(self):
		# In a page mode we show the page entirely
		if (self.m_usePageMode):

			pageHeight = self.m_pageMetrics.pxPageSize().height()
			documentHeight = pageHeight * self.document().pageCount()
			maximumValue = documentHeight - self.viewport().height()
			if (self.verticalScrollBar().maximum() != maximumValue):
				self.verticalScrollBar().setMaximum(maximumValue)
			
		# In normal mode, just add a little extra scrolling for convenience.
		else:
			SCROLL_DELTA = 800
			maximumValue = self.document().size().height() - self.viewport().size().height() + (SCROLL_DELTA if self.m_addBottomSpace else 0)
			if (self.verticalScrollBar().maximum() != maximumValue):
				self.verticalScrollBar().setMaximum(maximumValue)

	def paintPagesView(self):
		# This method paints the page layout, nothing more
		# It also paints the background at page breaks
		# The design is drawn only when the editor is in page mode.
		if (self.m_usePageMode):
			# Draw page breaks
			pageWidth = self.m_pageMetrics.pxPageSize().width()
			pageHeight = self.m_pageMetrics.pxPageSize().height()

			p = QPainter(self.viewport())
			borderPen = QPen(self.palette().dark(), 1)

			curHeight = pageHeight - (self.verticalScrollBar().value() % pageHeight)

			# Horizontal offset if there is a scroll bar
			horizontalDelta = self.horizontalScrollBar().value()

			# Paint page views while there are remotely more visible pages
			while (curHeight < pageHeight + self.height()):

				p.setRenderHint(QPainter.Antialiasing);
				path = QPainterPath()
				# In painting page, height of the rect is (pageHeight - 10)
				# to give page break
				pageLayout = QRectF(0 - horizontalDelta, curHeight - pageHeight, pageWidth, pageHeight - 10)
				path.addRect(pageLayout)
				p.fillPath(path, Qt.white)
				
				p.setPen(borderPen);
				p.drawPath(path)
				
				# Go to next page
				curHeight += pageHeight

	def paintPageNumbers(self):
		# Page numbers are drawn only when the editor is in page mode,
		# if fields are set and the option to display numbers is enabled
		if (self.m_usePageMode and not self.m_pageMetrics.pxPageMargins().isNull() and self.m_showPageNumbers):
			
			pageWidth = self.m_pageMetrics.pxPageSize().width()
			pageHeight = self.m_pageMetrics.pxPageSize().height()
			pageMargins = QMarginsF(self.m_pageMetrics.pxPageMargins())

			p = QPainter(self.viewport())
			font = QFont()
			font.setPointSize(10)
			font.setFamily('Calibri')
			p.setFont(font)
			p.setPen(QPen(self.palette().text(), 1))

			# The current height and width are displayed on the screen.
			curHeight = pageHeight - (self.verticalScrollBar().value() % pageHeight)

			# The start of the field must take into account the scrollbar offset.
			leftMarginPosition = pageMargins.left() - self.horizontalScrollBar().value()

			# Total field width
			marginWidth = pageWidth - pageMargins.left() - pageMargins.right()

			# The number of the first page to see.
			pageNumber = self.verticalScrollBar().value() / pageHeight + 1

			# Add 0.3 to pageNumber before emitting 
			# to announce page when it is about halfway up the screen
			self.pageInfo.emit((int(pageNumber + 0.3), int(self.verticalScrollBar().maximum() / pageHeight + 1)))

			# Paint page numbers while there are remotely more visible pages
			while(curHeight < pageHeight + self.height()):

				# Define the space for top page number; paint number
				topMarginRect = QRectF(leftMarginPosition, curHeight - pageHeight, marginWidth, pageMargins.top())
				self.paintPageNumber(p, topMarginRect, True, pageNumber)

				# Define the space for bottom page number; paint number
				bottomMarginRect = QRectF(leftMarginPosition, curHeight - pageMargins.bottom(), marginWidth, pageMargins.bottom())
				self.paintPageNumber(p, bottomMarginRect, False, pageNumber)

				# Go to next page
				pageNumber += 1
				curHeight += pageHeight

	def paintPageNumber(self, _painter, _rect, _isHeader, _number):
		# Top field
		if (_isHeader):
			# If the numbering is drawn in the top field
			if (self.m_pageNumbersAlignment & Qt.AlignTop):
				_painter.drawText(_rect, Qt.AlignVCenter | (self.m_pageNumbersAlignment ^ Qt.AlignTop), str(int(_number)))

		# Bottom field
		else:
			# If the numbering is drawn in the bottom field
			if (self.m_pageNumbersAlignment & Qt.AlignBottom):
				_painter.drawText(_rect, Qt.AlignVCenter | (self.m_pageNumbersAlignment ^ Qt.AlignBottom), str(int(_number)))


	@Slot(int, int)
	def aboutVerticalScrollRangeChanged(self, _minimum, _maximum):
		# Q_UNUSED(_minimum)

		# Update the viewport indents
		self.updateViewportMargins()


		scrollValue = self.verticalScrollBar().value()

		# If the current scroll position is greater than the maximum value,
		# then textedit updated the interval itself, apply its own correction function
		if (scrollValue > _maximum):
			self.updateVerticalScrollRange()

	def aboutDocumentChanged(self):
		if (self.m_document != self.document()):
			self.m_document = self.document()

			# Configuring the document size change check
			self.document().documentLayout().update.connect(self.aboutUpdateDocumentGeometry)

	def aboutUpdateDocumentGeometry(self):
		# Very important function
		# Determines the size of the document using the page metrics
		# TODO To adjust the width in non-paged mode, change the default self.width()
		# below to the desired width...
		documentSize = QSizeF(self.width() - self.verticalScrollBar().width(), -1)
		if (self.m_usePageMode):
			# This condition ensures that only the width and height in paged mode is adjusted
			pageWidth = self.m_pageMetrics.pxPageSize().width()
			pageHeight = self.m_pageMetrics.pxPageSize().height()
			documentSize = QSizeF(pageWidth, pageHeight)

		# Update document size
		if (self.document().pageSize() != documentSize):
			self.document().setPageSize(documentSize)

		# At the same time, set the indents
		# ... remove the document
		if (self.document().documentMargin() != 0):
			self.document().setDocumentMargin(0)

		# ... and adjust the document fields
		rootFrameMargins = self.m_pageMetrics.pxPageMargins()
		rootFrameFormat = self.document().rootFrame().frameFormat()
		if (rootFrameFormat.leftMargin() != rootFrameMargins.left() or rootFrameFormat.topMargin() != rootFrameMargins.top() or rootFrameFormat.rightMargin() != rootFrameMargins.right() or rootFrameFormat.bottomMargin() != rootFrameMargins.bottom()):
			rootFrameFormat.setLeftMargin(rootFrameMargins.left())
			rootFrameFormat.setTopMargin(rootFrameMargins.top())
			rootFrameFormat.setRightMargin(rootFrameMargins.right())
			rootFrameFormat.setBottomMargin(rootFrameMargins.bottom())
			self.document().rootFrame().setFrameFormat(rootFrameFormat)

	def setThemeColor(self, themeColor):
		self.verticalScrollBar().setStyleSheet(""" QScrollBar:vertical {
				border: none;
				background: """ + themeColor + """ ;
				width: 15px;
				margin: 20, 20, 0, 0;
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
				height: 20px;
				subcontrol-position: bottom;
				subcontrol-origin: margin;
				border-radius: 3px;
			}
			QScrollBar::sub-line:vertical {
				border: none;
				background: """ + themeColor + """ ;
				height: 20px;
				subcontrol-position: top;
				subcontrol-origin: margin;
				border-radius: 3px;
			}
			QScrollBar::add-line:vertical:hover, QScrollBar::sub-line:vertical:hover {
				background: #8f8f8f;
			}
			QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
				border: none;
				width: 5px;
				height: 5px;
				background: white;
			}
			QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
				background: none;
			} """)

		self.horizontalScrollBar().setStyleSheet(""" QScrollBar:horizontal {
				border: none;
				background: """ + themeColor + """ ;
				width: 12px;
				margin: 20, 0, 20, 0;
			}
			QScrollBar::handle:horizontal {
				background: #8f8f8f;
				min-height: 20px;
				border-radius: 3px;
			}
			QScrollBar::handle:horizontal:hover {
				background: white;
			}
			QScrollBar::add-line:horizontal {
				border: none;
				background: """ + themeColor + """ ;
				height: 20px;
				subcontrol-position: bottom;
				subcontrol-origin: margin;
			}
			QScrollBar::sub-line:horizontal {
				border: none;
				background: """ + themeColor + """ ;
				height: 20px;
				subcontrol-position: top;
				subcontrol-origin: margin;
			}
			QScrollBar::add-line:horizontal:hover, QScrollBar::sub-line:horizontal:hover {
				background: #8f8f8f;
			}
			QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
				border: none;
				width: 5px;
				height: 5px;
				background: white;
			}
			QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
				background: none;
			} """)


			
