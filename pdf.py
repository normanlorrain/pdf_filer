import base64
import fitz
import re

import util

currentFile = None

print(fitz.__doc__)


class pdf:
    def __init__(self, fname: str, status):
        self.name = fname
        self.status = status
        inputFile = open(fname, "rb")
        bytes = inputFile.read()
        inputFile.close()

        self.doc = fitz.Document(stream=bytes)

        self.page_count = len(self.doc)
        self.currentPage = 1

        self.status(f"PDF init: {fname}, {self.page_count} pages")

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
        self.status(f"{self.name} : page {self.currentPage}")
        bytes = pixmap.tobytes()
        enc = base64.b64encode(bytes)
        strEnc = enc.decode("ascii")
        return strEnc

    def pageDn(self):
        self.status(f"PDF pageDn: {self.name}")

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
        self.status(f"Scanning {self.doc.page_count} pages:", end="")
        for page in self.doc.pages():
            self.status(f" {page.number +1} ", end="")
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

            self.status(f"   NAME:  {last}, {first}")
            return (last, first)
        else:
            self.status(f"no name found.")
            return None


# Future enhancement: scan with pytesseract
# Rationale: pymupdf's implementation effectively renders the page at a lower resolution
# than the images in the pdf.  Since we're dealing with faxes (scans) we
# should get better results by pulling the full resolution images from
# the pdf and calling pytesseract ourselves.  I've confirmed this works, but would
# like to test further.
############################################################
# import fitz
# import pytesseract
# from io import BytesIO


# from PIL import Image
# images = doc.get_page_images(1)

# for (xref, _, _, _, _, _, _, _, _)  in images:
#     img = doc.extract_image(xref=xref)
#     bytes = BytesIO( initial_bytes=img['image'])
#     img = Image.open(bytes) #,size=(width,height)
#     img.save(f'PIL_xref {xref}.png')
#     text = pytesseract.image_to_string(img)


#     pass
