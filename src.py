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
src = config.config['INPUT']['SOURCE']


fileList = {}


def init():
    global fileIterator 
    listFiles()
    scanFiles()
    fileIterator = iter(fileList)

# def getNextFile():
#     for item in  fileList.items():
#         print(f"getNextFile: {item}")
#         yield item
        


def listFiles():
    for fname in glob.glob(f'{src}\\*.pdf'):
        fileList[fname] = None

def scanFiles():
    for fname in fileList:
        scanFile(fname)


def scanFile(fname):
    print(fname, end=' ')
    inputFile = open(fname, "rb")
    bytes = inputFile.read()
    inputFile.close()

    fileList[fname] = scanPDFContents(bytes)

def scanPDFContents(bytes):

    doc = fitz.Document(stream=bytes)
    # page = doc.load_page(4)
    match = None
    for page in doc.pages():
        print(f" {page.number} ", end='')
        textpage = page.get_textpage_ocr( tessdata="C:\\Program Files\\Tesseract-OCR\\tessdata")
        contents = textpage.extractText()
        match = re.search(r".*\nRE:\s*(.*)\n.*", contents)  # r".*\nRE:\s*(\w+),?\s*(\w+).*"
        if match:
            break
        match = re.search(r".*\nPatient[\W\s]+(.*)\n.*", contents,flags=re.IGNORECASE)  # Patient[\W\s]*([\s\w']+),?\s*(\w+).
        if match:
            break
        match = re.search(r".*\nTo the parents of:[\W\s]*(.*)\n.*", contents) 
        if match:
            break

    if match:
        # (last, first) 
        fullName = match.group(1)
        (last,first) = util.splitName(fullName)
        
        print(f"   NAME:  {last}, {first}")
        return (last,first)
    else:
        print(f"no name found.")
        return None




if __name__ == '__main__':
    init()
    pass