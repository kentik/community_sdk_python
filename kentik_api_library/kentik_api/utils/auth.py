import json
import logging
import os
from functools import lru_cache
from typing import Dict, Optional, Tuple

log = logging.getLogger("auth")


@lru_cache
def load_credential_profile(profile: str) -> Dict:
    home: str = os.environ.get("KTAPI_HOME", os.environ.get("HOME", "."))
    filename = os.environ.get("KTAPI_CFG_FILE", os.path.join(home, ".kentik", profile))
    try:
        with open(filename) as f:
            try:
                cfg = json.load(f)
            except json.decoder.JSONDecodeError as ex:
                log.critical(
                    "Failed to parse JSON in profile file '%s' (exception: %s)",
                    filename,
                    ex,
                )
                return {}
    except OSError as e:
        log.critical("Cannot open config file: %s (%s)", filename, str(e))
        return {}
    ok: bool = True
    # check for required keys
    for key in ("email", "api-key"):
        if key not in cfg:
            log.critical("No '%s' in config file: %s", key, filename)
            ok = False
    if ok:
        return cfg
    else:
        return {}


def get_credentials(profile: str = "default") -> Tuple[str, str]:
    email = os.environ.get("KTAPI_AUTH_EMAIL")
    token = os.environ.get("KTAPI_AUTH_TOKEN")
    if email is None or token is None:
        cfg = load_credential_profile(profile)
        if cfg:
            email = cfg["email"]
            token = cfg["api-key"]
    if email and token:
        return email, token
    else:
        raise RuntimeError("Failed to get API authentication credentials")


def get_url(profile: str = "default") -> Optional[str]:
    return os.environ.get("KTAPI_URL", load_credential_profile(profile).get("url"))


def get_proxy(profile: str = "default") -> Optional[str]:
    return os.environ.get("KTAPI_PROXY", load_credential_profile(profile).get("proxy"))
