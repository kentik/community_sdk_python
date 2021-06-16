#!/usr/bin/python3
import logging
import pandas as pd
import numpy as np
import sys
import typer
from datetime import (datetime, timedelta, timezone)
from kentik_api import KentikAPI, QueryDefinition, QuerySQL
from kentik_api.analytics import *
from kentik_api.utils import DeviceCache, DFCache, get_credentials
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()
api: Optional[KentikAPI] = None


def start_shell(profile: str) -> None:
    from traitlets.config.loader import Config
    from IPython.terminal.embed import InteractiveShellEmbed
    from IPython.terminal.prompts import Prompts, Token

    class CliPrompt(Prompts):
        def in_prompt_tokens(self, cli=None):
            return [(Token, f'({profile})'), (Token.Prompt, ' > ')]

    cfg = Config()
    cfg.InteractiveShell.color_info = True

    shell = InteractiveShellEmbed(config=cfg)
    shell.prompts = CliPrompt(shell)
    shell()


def debug_on() -> int:
    current_level = log.getEffectiveLevel()
    log.setLevel(logging.DEBUG)
    log.debug('Debug messages enabled (previous level: %d)', current_level)
    return current_level


def debug_off(level: int = logging.INFO) -> None:
    log.debug('Disabling debug messages (setting level: %d)', level)
    log.setLevel(level)


def log_to(filename):
    log.debug('Switching log output to: %s', filename)
    log.removeHandler(log.handlers[0])
    if type(filename) == str:
        log.addHandler(logging.FileHandler(filename))
    else:
        log.addHandler(logging.StreamHandler(filename))


def main(profile: str = typer.Argument('default', help="Credential profile"),
         debug: bool = typer.Option(False, '-d', '--debug', help="Debug output"),
         proxy: Optional[str] = typer.Option(None, '--proxy', help="Proxy to use to connect to API")) -> None:
    global api

    if debug:
        log.setLevel(logging.DEBUG)
        log.debug('Debug output enabled')

    email, token = get_credentials(profile)
    if email is None or token is None:
        log.critical("Failed to get API credentials")
        sys.exit(1)
    print('using credential profile: ', profile)
    print('email: ', email)
    print()

    api = KentikAPI(email, token, proxy=proxy)
    start_shell(profile)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    typer.run(main)
