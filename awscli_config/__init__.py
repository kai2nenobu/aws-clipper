from __future__ import annotations

from typing import Any, TextIO

import yaml


def _subst_variables(dic: dict[str, Any], variables: dict[str, Any]) -> dict[str, Any]:
    return {k: v.format(**variables) if isinstance(v, str) else v for k, v in dic.items()}


def convert(instream: TextIO, outstream: TextIO) -> None:
    config = yaml.safe_load(instream)
    if config is None:
        return  # nothing to do
    default_settings = config.get("default", {})
    profiles = {}
    for name, prof in config.get("profiles", {}).items():
        prof = {} if prof is None else prof
        target_profiles = prof.pop("target_profiles", {})
        target_profile_default = prof.pop("target_profile_default", {})
        merged_prof = default_settings | prof
        profiles[name] = _subst_variables(merged_prof, {"profile": name})
        for target_name, target_prof in target_profiles.items():
            target_prof = {} if target_prof is None else target_prof
            merged_target_prof = default_settings | target_profile_default | {"source_profile": name} | target_prof
            profiles[target_name] = _subst_variables(merged_target_prof, {"profile": target_name})
    # print(list(profiles))
    for name, prof in profiles.items():
        prof_name = "[default]" if name == "default" else f"[profile {name}]"
        outstream.write(prof_name + "\n")
        for k, v in prof.items():
            outstream.write(f"{k} = {v}\n")
        outstream.write("\n")
