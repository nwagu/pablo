
"""This class contains the method that converts a html document to pbl
to optimize it for the Pablo application."""

from lxml import etree

class HTMLCleaner():

    def clean(html):

        root = etree.HTML(html)


        pbl = etree.tostring(root, pretty_print=True, method="html")

        return pbl