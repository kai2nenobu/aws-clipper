from __future__ import annotations

import configparser
from typing import Any, TextIO

import yaml

# This version is placeholder. The actual version is populated by poetry-dynamic-versioning
__version__ = "0.0.0"


def _subst_variables(dic: dict[str, Any], variables: dict[str, Any]) -> dict[str, Any]:
    return {k: v.format(**variables) if isinstance(v, str) else v for k, v in dic.items() if v is not None}


def convert(instream: TextIO, outstream: TextIO) -> None:
    config = yaml.safe_load(instream)
    if config is None:
        return  # nothing to do
    default_settings = config.get("default", {})
    profiles = {}
    for name, prof in config.get("profiles", {}).items():
        prof = {} if prof is None else prof
        merged_prof = {**default_settings, **prof}
        profiles[name] = _subst_variables(merged_prof, {"profile": name})
    for group_name, group_config in config.get("groups", {}).items():
        group_default = group_config.get("default", {})
        group_profile_name = group_config.get("profile_name", "{name}")
        for name, prof in group_config.get("profiles", {}).items():
            prof = {} if prof is None else prof
            merged_prof = {
                **default_settings,
                **group_default,
                **prof,
            }
            profile_name = group_profile_name.format(group=group_name, name=name)
            profiles[profile_name] = _subst_variables(merged_prof, {"profile": profile_name})
    # output with ini format
    config = configparser.ConfigParser()
    for name, prof in profiles.items():
        section_name = "default" if name == "default" else f"profile {name}"
        config[section_name] = prof
    config.write(outstream)
