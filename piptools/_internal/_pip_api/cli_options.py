"""
Tools for parsing pip CLI options.
"""

from __future__ import annotations

import optparse

from pip._internal.cli import cmdoptions


def postprocess_cli_options(options: optparse.Values) -> None:
    """
    After CLI parsing, pip processes options further to check various constraints and
    coalesce values. Emulate and/or invoke those same behaviors.
    """
    cmdoptions.check_release_control_exclusive(options)
