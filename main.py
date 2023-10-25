# import flet as ft
import fitz 
# from PIL import Image

import pytesseract


# import pdf

import sys
import re
import glob

pdfFile = None

img = None

src = "M:\\Everyone\\faxes - NL\\"
for fname in glob.glob(f'{src}\\*.pdf'):
    # fname = "M:\\Everyone\\faxes - NL\\20231023131133-7880_04.pdf"
    # fname = "M:\\Everyone\\faxes - NL\\20231014083105-2052_05.pdf"
    # fname = "M:\\Everyone\\faxes - NL\\20231016075314-8757_01.pdf"
    print(fname, end=' ')
    inputFile = open(fname, "rb")
    bytes = inputFile.read()
    inputFile.close()

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
        names = re.findall(r"[\w']+", fullName)

        last=''
        first=''

        if ',' in fullName:
            last,first = fullName.split(',')
            # first = ' '.join(names)
        elif any(map(str.isupper, names)):
            for name in names:
                if name.isupper():
                    last = name
                else:
                    first+=name
                    first += ' '
        else:
            last = names[-1]
            first = ' '.join(names[:-1])



        # last = ''
        # first = ''
        # for name in names:
        #     if name.isupper():
        #         last = name

        last = last.upper().strip()
        first = first.strip()
        print(f"   NAME:  {last}, {first}")
    else:
        print(f"no name found.")



