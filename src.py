# import flet as ft
import fitz

# from PIL import Image

import pytesseract


# import pdf

import sys
import re
import glob

import util
import config


pdfFile = None

img = None
scrDir = config.config["SRC"]["DIR"]


filename_nameTuple_dict = {}


def init():
    listFiles()
    global fileIterator
    fileIterator = iter(filename_nameTuple_dict)


def getNextFile():
    return next(fileIterator)


#     for item in  filename_nameTuple_dict.items():
#         print(f"getNextFile: {item}")
#         yield item


# def getNameTuple(path):
#     return filename_nameTuple_dict[path]


def listFiles():
    global filename_nameTuple_dict
    filename_nameTuple_dict = {}
    for fname in glob.glob(f"{scrDir}\\*.pdf"):
        filename_nameTuple_dict[fname] = None


# def scanFiles():
#     for fname in filename_nameTuple_dict:
#         scanFile(fname)


def scanFile(fname):
    print(fname, end=" ")
    inputFile = open(fname, "rb")
    bytes = inputFile.read()
    inputFile.close()

    filename_nameTuple_dict[fname] = scanPDFContents(bytes)


def scanPDFContents(bytes):
    doc = fitz.Document(stream=bytes)
    # page = doc.load_page(4)
    match = None
    for page in doc.pages():
        print(f" {page.number} ", end="")
        textpage = page.get_textpage_ocr(
            tessdata="C:\\Program Files\\Tesseract-OCR\\tessdata"
        )
        contents = textpage.extractText()
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
        match = re.search(r".*\nTo the parents of:[\W\s]*(.*)\n.*", contents)
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
