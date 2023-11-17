import glob
from typing import Iterator

import config

scrDir = config.config["SRC"]["DIR"]
_iterator: Iterator


def init():
    global _iterator
    _iterator = listFiles()


def getNextFile():
    return next(_iterator)


def listFiles():
    for fname in glob.glob(f"{scrDir}\\*.pdf"):
        yield fname


if __name__ == "__main__":
    init()
    while True:
        try:
            path = getNextFile()
            print(path)
        except StopIteration:
            print("no more files.  Restarting.")
            init()
    pass
