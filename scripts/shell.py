#!/usr/bin/env python3
from __future__ import annotations

import datetime
import os
import pathlib
import platform
import sys

from distutils.version import LooseVersion

NEULABS_PATH = pathlib.Path(os.getenv('HOME'), '.neulabs')

RC = """
# AZIONA CONFIG (configured in %s)
source %s/.env
source ${NEULABS_ACTIVE_PERSISTENT_PATH:-}
export PATH=$PATH:$NEULABS_BIN_PATH
# AZIONA CONFIG END
""" % (datetime.datetime.now(), NEULABS_PATH)


def _configurations():
    def write_conf(filename: str):
        if not os.path.isfile(filename):
            with open(filename, 'w') as f:
                f.write(RC)
            return

        with open(filename, 'r') as f:
            if 'AZIONA CONFIG' not in f.read():
                with open(filename, 'a') as f:
                    f.write(RC)

    shell = os.environ.get('SHELL', '').split('/')[-1]

    if shell == 'bash':
        return write_conf(pathlib.Path(os.getenv('HOME'), '.bashrc'))

    if shell == 'zsh':
        return write_conf(pathlib.Path(os.getenv('HOME'), '.zshrc'))

    print('Add to shell configuration file: \n' + RC + '\n')


def main():
    try:
        py_version = LooseVersion(platform.python_version())
        if py_version < '3.6':
            raise RuntimeError('PY Version required >= 3.8')

        _configurations()
    except KeyboardInterrupt:
        return 0


if __name__ == '__main__':
    sys.exit(main())
