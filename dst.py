import datetime
import glob
import util
import os
import config as cfg
import difflib

# difflib.get_close_matches


config = cfg.config

patientFolders = {}


def init():
    for user in config:
        if user == "INPUT":
            continue
        root = config[user]["dst"]
        for folder in glob.glob("*", root_dir=root):
            (last, first) = util.splitName(folder)
            patientFolders[f"{last}::{first}"] = os.path.join(root, folder)


def getName(last: str, first: str):
    if f"{last}::{first}" in patientFolders:
        return patientFolders[f"{last}::{first}"]
    else:
        return None


def generateDstName(path, description):
    format = "%Y%m%d"
    date = datetime.datetime.strptime(path[0:8], format).date()
    return f'{description} {date.strftime("%b %d %Y")}'


if __name__ == "__main__":
    print(generateDstName("20231014083105-2052_05.pdf", "Rx sent"))


if __name__ == "__main__":
    pass
