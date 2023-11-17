import glob
from typing import Iterator

import config

scrDir = config.config["SRC"]["DIR"]
_iterator: Iterator


def init():
    global _iterator
    _iterator = iter(glob.glob(f"{scrDir}\\*.pdf"))


def getNextFile():
    return next(_iterator)


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
