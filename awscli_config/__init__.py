from typing import TextIO

import yaml


def _subst_variables(dic: dict, variables: dict):
    return {
        k: v.format(**variables) if isinstance(v, str) else v
        for k, v in dic.items()
    }


def convert(instream: TextIO, outstream: TextIO):
    config = yaml.safe_load(instream)
    if config is None:
        return # nothing to do
    default_settings = config.get("default", {})
    profiles = {}
    for name, prof in config.get("profiles", {}).items():
        prof = {} if prof is None else prof
        prof = _subst_variables(prof, {"profile": name})
        target_profiles = prof.pop("target_profiles", {})
        target_profile_default = prof.pop("target_profile_default", {})
        profiles[name] = default_settings | prof
        for target_name, target_prof in target_profiles.items():
            target_prof = _subst_variables(target_prof, {"profile": name})
            profiles[target_name] = default_settings | target_profile_default | {"source_profile": name} | target_prof
    #print(list(profiles))
    for name, prof in profiles.items():
        prof_name = "[default]" if name == "default" else f"[profile {name}]"
        outstream.write(prof_name + "\n")
        for k, v in prof.items():
            outstream.write(f"{k} = {v}\n")
        outstream.write("\n")
