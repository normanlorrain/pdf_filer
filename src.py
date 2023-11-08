import re
import glob

import fitz

import util
import config

scrDir = config.config["SRC"]["DIR"]
filename_nameTuple_dict = {}


def init():
    listFiles()
    global fileIterator
    fileIterator = iter(filename_nameTuple_dict)


def getNextFile():
    return next(fileIterator)


def listFiles():
    global filename_nameTuple_dict
    filename_nameTuple_dict = {}
    for fname in glob.glob(f"{scrDir}\\*.pdf"):
        filename_nameTuple_dict[fname] = None


def scanFile(fname):
    print(f"Scanning file {fname}")
    inputFile = open(fname, "rb")
    bytes = inputFile.read()
    inputFile.close()

    filename_nameTuple_dict[fname] = scanPDFContents(bytes)


def scanPDFContents(bytes):
    doc = fitz.Document(stream=bytes)
    # page = doc.load_page(4)
    match = None
    print(f"Scanning {doc.page_count} pages:", end="")
    for page in doc.pages():
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


if __name__ == "__main__":
    init()
    pass
