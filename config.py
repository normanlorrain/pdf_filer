import tomllib

with open("config.toml", "rb") as fp:
    config = tomllib.load(fp)

# Used to be in the config file.  Hard-code it.
config["TYPES"]["other"] = "{other} faxed {date}"

pass
