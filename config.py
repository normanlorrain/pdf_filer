import tomllib
from pathlib import Path


SRC = "SRC"
DIR = "DIR"
DST = "DST"
TYPES = "TYPES"
OTHER = "other"

CONFIG_FILE = "config.toml"

with open(CONFIG_FILE, "rb") as fp:
    config = tomllib.load(fp)

# Used to be in the config file.  Hard-code it.
config[TYPES][OTHER] = "{other} faxed {date}"

# Validate configuration
if not Path(config[SRC][DIR]).exists():
    raise Exception(
        f"{CONFIG_FILE}:\n[{SRC}]\n    {config[SRC][DIR]} <---- PATH DOESN'T EXIST "
    )

for user, path in config[DST].items():
    if not Path(path).exists():
        raise Exception(f"{CONFIG_FILE}:\n    {user} = {path} <---- PATH DOESN'T EXIST")

pass
