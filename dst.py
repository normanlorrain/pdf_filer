import glob
import util
import os
import config as cfg

config = cfg.config

patientFolders={}
for user in config:
    if user=='INPUT':
        continue
    root = config[user]['dst']
    for folder in glob.glob("*", root_dir=root):
        (last,first) = util.splitName( folder )
        patientFolders[f'{last}::{first}'] = os.path.join(root,folder)

if __name__ == '__main__':
    pass