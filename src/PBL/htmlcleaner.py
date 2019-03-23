
"""This class contains the method that converts a html document to pbl
to optimize it for the Pablo application."""

from lxml import etree, html

class HTMLCleaner():

    def clean(input):

        root = etree.HTML(input)
        # root = html.fromstring(input)
        root.tag = "pbl"

        pbl = etree.tostring(root, pretty_print=True, method="html")

        return pbl