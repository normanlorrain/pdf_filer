from pathlib import Path
import difflib
import datetime
import glob
import os

import util
import config as cfg

dstUsers = cfg.config["DST"]

patientFolders: dict[str, str] = {}


def init():
    for root in dstUsers.values():
        for folder in glob.glob("*", root_dir=root):
            folder_path = os.path.join(root, folder)
            if os.path.isdir(folder_path):
                (last, first) = util.splitName(folder)
                patientFolders[f"{last}::{first}"] = folder_path
            else:
                print(f"Warning: {folder_path} is not a directory")
            


# def getName(last: str, first: str):
#     if f"{last}::{first}" in patientFolders:
#         return patientFolders[f"{last}::{first}"]
#     else:
#         return None


def getCloseNames(last: str, first: str) -> list[tuple[str, str]]:
    closeNames = difflib.get_close_matches(f"{last}::{first}", patientFolders)
    return list(map(lambda name: (name, patientFolders[name]), closeNames))


def generateDstDate(unknownPath: str) -> str:
    path = Path(unknownPath).name
    format = "%Y%m%d"
    date = datetime.datetime.strptime(path[0:8], format).date()
    return date.strftime("%b %d %Y")


if __name__ == "__main__":
    print(generateDstDate("20231014083105-2052_05.pdf"))
    print(generateDstDate("C:\\TEMP\\20241014083105-2052_05.pdf"))

if __name__ == "__main__":
    init()

    pass
