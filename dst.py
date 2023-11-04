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


if __name__ == "__main__":
    pass
