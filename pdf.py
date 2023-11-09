import base64
import fitz
import re

import util

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

        print(f"PDF init: {fname}, {self.page_count} pages")

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
        print(f"PDF pageDn: {self.name}")

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

    def scanForName(self):
        # doc = fitz.Document(stream=bytes)
        # page = doc.load_page(4)
        match = None
        print(f"Scanning {self.doc.page_count} pages:", end="")
        for page in self.doc.pages():
            print(f" {page.number +1} ", end="")
            textpage = page.get_textpage_ocr(
                tessdata="C:\\Program Files\\Tesseract-OCR\\tessdata",
                full=True,
                dpi=300,
                # flags= 0
            )
            contents = textpage.extractText()
            # contents=page.get_text(textpage=textpage)
            match = re.search(
                r".*\nRE:\s*(.*)\n.*", contents, flags=re.IGNORECASE
            )  # r".*\nRE:\s*(\w+),?\s*(\w+).*"
            if match:
                break
            match = re.search(
                r".*\nPatient[\W\s]+(.*)\n.*", contents, flags=re.IGNORECASE
            )  # Patient[\W\s]*([\s\w']+),?\s*(\w+).
            if match:
                break
            match = re.search(r".*\nTo the parents of:?[\W\s]*(.*)\n.*", contents)
            if match:
                break

        if match:
            # (last, first)
            fullName = match.group(1)
            (last, first) = util.splitName(fullName)

            print(f"   NAME:  {last}, {first}")
            return (last, first)
        else:
            print(f"no name found.")
            return None
