import json
import logging
import os
from typing import Dict, Optional, Tuple


def load_credential_profile(filename: str) -> Optional[Dict]:
    try:
        with open(filename) as f:
            cfg = json.load(f)
    except OSError as e:
        logging.critical("Cannot open config file: %s (%s)", filename, str(e))
        return None
    ok: bool = True
    for key in ("email", "api-key"):
        if key not in cfg:
            logging.critical("No '%s' in config file: %s", key, filename)
            ok = False
    if ok:
        return cfg
    else:
        return None


def get_credentials(profile: str = "default") -> Tuple[str, str]:
    email = os.environ.get("KTAPI_AUTH_EMAIL")
    token = os.environ.get("KTAPI_AUTH_TOKEN")
    home: str = os.environ.get("KTAPI_HOME", os.environ.get("HOME", "."))
    if email is None or token is None:
        cfg = load_credential_profile(os.environ.get("KTAPI_CFG_FILE", os.path.join(home, ".kentik", profile)))
        if cfg is not None:
            email = cfg["email"]
            token = cfg["api-key"]
    if email and token:
        return email, token
    else:
        raise RuntimeError("Failed to get API authentication credentials")
