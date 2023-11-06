import sys
import base64
import fitz
import pathlib
import os

currentFile = None

print(fitz.__doc__)

width, height = fitz.paper_size("letter")


class pdf:
    def __init__(self, fname):
        self.name = fname
        inputFile = open(fname, "rb")
        bytes = inputFile.read()
        inputFile.close()

        self.doc = fitz.Document(stream=bytes)

        self.page_count = len(self.doc)
        self.currentPage = 1

        title = "PyMuPDF display of '%s', pages: %i" % (fname, self.page_count)

    def __del__(self):
        pass

    # read the page data
    def get_page(self):
        global width, height
        zoom = 2
        pixmap = self.doc.get_page_pixmap(  # type: ignore
            self.currentPage - 1, matrix=fitz.Matrix(zoom, zoom)
        )  # *, matrix: matrix_like = Identity, dpi=None, colorspace: Colorspace = csRGB, clip: rect_like = None, alpha: bool = False, annots: bool = True)
        width = pixmap.width
        height = pixmap.height
        print(f"get page {self.currentPage}: {width} x {height}")
        bytes = pixmap.tobytes()
        enc = base64.b64encode(bytes)
        strEnc = enc.decode("ascii")
        return strEnc

    def pageDn(self):
        if self.currentPage < self.doc.page_count:
            self.currentPage += 1

    def pageUp(self):
        if self.currentPage > 1:
            self.currentPage -= 1

    def rotate(self):
        current_rotation = self.doc[self.currentPage].rotation
        new_rotation = (current_rotation + 180) % 360
        self.doc[self.currentPage].set_rotation(new_rotation)

    def save(self):
        # self.backup.keep = True
        self.doc.save(self.name)
