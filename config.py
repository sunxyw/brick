from dynaconf import Dynaconf
from dynaconf.loaders.toml_loader import write

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['settings.toml', '.secrets.toml'],
)


def write_config(key: str, value: str):
    """Write configuration to toml file. Nested keys are supported."""
    # check if key is nested
    if "." in key:
        key_list = key.split(".")
        key = key_list[0]
        nested_key = ".".join(key_list[1:])
        # ensure parent key exists
        merging_setting = {key: {nested_key: value}}
    else:
        merging_setting = {key: value}
    write("settings.toml", merging_setting, merge=True)
    # reload config
    settings.reload()
