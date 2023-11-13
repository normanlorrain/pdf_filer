import glob

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


# def scanFile(fname):
#     print(f"Scanning file {fname}")
#     inputFile = open(fname, "rb")
#     bytes = inputFile.read()
#     inputFile.close()

#     filename_nameTuple_dict[fname] = scanPDFContents(bytes)


if __name__ == "__main__":
    init()
    pass
