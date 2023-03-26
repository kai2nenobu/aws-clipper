from __future__ import annotations

from typing import Any, TextIO

import yaml


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
    for _, group_config in config.get("groups", {}).items():
        group_default = group_config.get("default", {})
        for name, prof in group_config.get("profiles", {}).items():
            prof = {} if prof is None else prof
            merged_prof = {
                **default_settings,
                **group_default,
                **prof,
            }
            profiles[name] = _subst_variables(merged_prof, {"profile": name})
    # print(list(profiles))
    for name, prof in profiles.items():
        prof_name = "[default]" if name == "default" else f"[profile {name}]"
        outstream.write(prof_name + "\n")
        for k, v in prof.items():
            outstream.write(f"{k} = {v}\n")
        outstream.write("\n")
