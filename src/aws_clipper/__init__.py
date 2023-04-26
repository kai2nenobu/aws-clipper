from __future__ import annotations

import configparser
from typing import Any, TextIO

import yaml

__version__ = "0.0.6"


def _expand_value(v: Any, variables: dict[str, Any] = {}) -> str:
    """
    In AWS CLI config, nested settings (like S3 settings) are indented as below.

    [default]
    s3 =
        max_concurrent_requests = 20
        max_queue_size = 10000

    So, insert a newline at beginning of multiline string in this function.
    """
    if isinstance(v, dict):
        return "\n" + "\n".join([f"{subkey} = {_expand_value(subvalue, variables)}" for subkey, subvalue in v.items()])
    if isinstance(v, list):
        return "\n" + "\n".join(v)
    elif isinstance(v, str):
        return v.format(**variables)
    elif isinstance(v, bool):
        return str(v).lower()
    else:
        return str(v)


def _expand_settings(dic: dict[str, Any], variables: dict[str, Any]) -> dict[str, Any]:
    """Expand settings into a format suitable for AWS CLI"""
    return {
        k: _expand_value(v, variables)
        for k, v in dic.items()
        # null value is suppressed
        if v is not None
    }


def _deep_merge(*dicts: dict[Any, Any]) -> dict[Any, Any]:
    """Merge multiple dictionaries deeply."""
    merged: dict[Any, Any] = {}
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
        profiles[name] = _expand_settings(merged_prof, {"profile": name})
    for group_name, group_config in config.get("groups", {}).items():
        group_default = group_config.get("default", {})
        group_profile_name = group_config.get("profile_name", "{name}")
        for name, prof in group_config.get("profiles", {}).items():
            prof = {} if prof is None else prof
            merged_prof = _deep_merge(default_settings, group_default, prof)
            profile_name = group_profile_name.format(group=group_name, name=name)
            profiles[profile_name] = _expand_settings(merged_prof, {"profile": profile_name})
    # output with ini format
    config = configparser.ConfigParser()
    for name, prof in profiles.items():
        section_name = "default" if name == "default" else f"profile {name}"
        config[section_name] = prof
    config.write(outstream)
