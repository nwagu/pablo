
"""This class contains the method that converts a html document to pbl
to optimize it for the Pablo application."""

from lxml import etree

class HTMLCleaner():

    def clean(html):
        pbl = html
        pbl = pbl.replace('<html>', '<pbl>')
        pbl = pbl.replace('</html>', '</pbl>')

        return pbl