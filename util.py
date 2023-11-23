import re
import sys
from pathlib import Path


def splitName(fullName: str) -> tuple[str, str]:
    names = re.findall(r"[\w']+", fullName)

    last = ""
    first = ""

    if len(names) == 1:  # BugsBUNNY
        names = re.findall(r"([A-Z][^A-Z]+|[A-Z]+)", fullName)
        if len(names) == 1:
            return (fullName, "")  # No split; single word name; give up!
        else:
            return splitName(" ".join(names[1:] + names[0:1]))  # Now "BUNNY Bugs"

    if "," in fullName:
        last, first = fullName.split(",", 1)
        # first = ' '.join(names)
    elif any(map(str.isupper, names)):
        for name in names:
            if name.isupper():
                last += name
                last += " "
            else:
                first += name
                first += " "
    else:
        last = names[-1]
        first = " ".join(names[:-1])

    last = last.upper().strip()
    first = first.strip()
    return (last, first)


# For projects with PyInstaller
# See https://www.pyinstaller.org/en/stable/runtime-information.html#run-time-information
def findDataFile(filename: str) -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        print("running in a PyInstaller bundle")
        return Path(sys._MEIPASS).joinpath(filename)  # type: ignore
    else:
        print("running in a normal Python process")
        return Path(__file__).parent.joinpath(filename)


# e.g. c:\folder\folder\{stem}.pdf
def incrementStem(stem: str) -> str:
    match = re.match(r"(.*)\((\d+)\)$", stem)
    if match:
        i = int(match.group(2)) + 1
        incremented = f"{match.group(1)}({i})"
    else:
        incremented = stem + "(1)"
    return incremented


def generateSafeFilename(dstFile):
    i = 1
    while dstFile.exists():
        suffix = dstFile.suffix
        stem = dstFile.stem  # e.g. c:\folder\folder\{stem}.pdf
        newStem = incrementStem(stem)
        # status(f"Destination file exists.  Trying new stem: {newStem}")
        dstFile = dstFile.with_stem(newStem)
    return dstFile


if __name__ == "__main__":
    print(incrementStem("foobar"))
    print(incrementStem("foobar(1)"))

    print(splitName("BUNNY"))
    print(splitName("BugsBUNNY"))
    print(splitName("bunny, bugs"))
    print(splitName("Bunny,Bugs"))
    print(splitName("BUNNY Bugs"))
    print(splitName("The Martian, Marvin"))
    print(splitName("THE MARTIAN, Marvin"))
    print(splitName("THE MARTIAN Marvin"))
