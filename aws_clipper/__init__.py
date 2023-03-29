from __future__ import annotations

import configparser
from typing import Any, TextIO

import yaml

# This version is placeholder. The actual version is populated by poetry-dynamic-versioning
__version__ = "0.0.0"


def _expand_value(v: Any, variables: dict[str, Any] = {}) -> str:
    if isinstance(v, dict):
        # This doesn't work as AWS CLI config
        #
        # [default]
        # s3 = max_concurrent_requests = 20
        #     max_queue_size = 10000
        #
        # This does work
        #
        # [default]
        # s3 =
        #     max_concurrent_requests = 20
        #     max_queue_size = 10000
        #
        # So, insert newline at beginning of multiline string
        return "".join([f"\n{subkey} = {_expand_value(subvalue, variables)}" for subkey, subvalue in v.items()])
    elif isinstance(v, str):
        return v.format(**variables)
    elif isinstance(v, bool):
        return str(v).lower()
    else:
        return str(v)


def _subst_variables(dic: dict[str, Any], variables: dict[str, Any]) -> dict[str, Any]:
    return {k: _expand_value(v, variables) for k, v in dic.items() if v is not None}


def _deep_merge(*dicts: dict[Any, Any]) -> dict[Any, Any]:
    """Merge multiple dictionaries deeply."""
    merged = {}
    for dic in dicts:
        for k, v in dic.items():
            current_v = merged.get(k)
            if isinstance(current_v, dict) and isinstance(v, dict):
                v = _deep_merge(current_v, v)
            merged[k] = v
    return merged


def convert(instream: TextIO, outstream: TextIO) -> None:
    config = yaml.safe_load(instream)
    if config is None:
        return  # nothing to do
    default_settings = config.get("default", {})
    profiles = {}
    for name, prof in config.get("profiles", {}).items():
        prof = {} if prof is None else prof
        merged_prof = _deep_merge(default_settings, prof)
        profiles[name] = _subst_variables(merged_prof, {"profile": name})
    for group_name, group_config in config.get("groups", {}).items():
        group_default = group_config.get("default", {})
        group_profile_name = group_config.get("profile_name", "{name}")
        for name, prof in group_config.get("profiles", {}).items():
            prof = {} if prof is None else prof
            merged_prof = _deep_merge(default_settings, group_default, prof)
            profile_name = group_profile_name.format(group=group_name, name=name)
            profiles[profile_name] = _subst_variables(merged_prof, {"profile": profile_name})
    # output with ini format
    config = configparser.ConfigParser()
    for name, prof in profiles.items():
        section_name = "default" if name == "default" else f"profile {name}"
        config[section_name] = prof
    config.write(outstream)
