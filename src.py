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


if __name__ == "__main__":
    init()
    pass
