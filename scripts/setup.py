#!/usr/bin/env python3
from __future__ import annotations

import datetime
import os
import pathlib
import platform
import sys

from distutils.version import LooseVersion

AZIONA_PATH = pathlib.Path(os.getenv('HOME'), '.aziona')
NEULABS_PATH = pathlib.Path(os.getenv('HOME'), '.neulabs')

if platform.system() == 'Darwin':
    NEULABS_WORKSPACE = pathlib.Path(os.getenv('HOME') + 'Documents/projects')
if platform.system() == 'Linux':
    NEULABS_WORKSPACE = pathlib.Path(os.getenv('HOME'), 'projects')

AZIONA_WORKSPACE = pathlib.Path(NEULABS_WORKSPACE, 'azionaventures')

ENV = {
    'NEULABS_DEVOPS_SUITE_VERSION': '1.0',
    'NEULABS_ACTIVE_PATH': '/tmp/.neulabs_active',
    'NEULABS_PATH': NEULABS_PATH,
    'NEULABS_ENV_PATH': pathlib.Path(NEULABS_PATH, '.env'),
    'NEULABS_ACTIVE_PERSISTENT_PATH': pathlib.Path(NEULABS_PATH, '.neulabs_active_perisistent'),
    'NEULABS_BIN_PATH': pathlib.Path(NEULABS_PATH, 'bin'),
    'NEULABS_MODULES_PATH': pathlib.Path(NEULABS_PATH, 'modules'),
    'NEULABS_TENANT_PATH': pathlib.Path(NEULABS_PATH, 'tenant'),
    'NEULABS_WORKSPACE': NEULABS_WORKSPACE,
    'AZIONA_PATH': AZIONA_PATH,
    'AZIONA_TERRAFORM_MODULES_PATH': pathlib.Path(AZIONA_PATH, 'terraform-modules'),
    'PROJECT_INFRASTRUCTURE': pathlib.Path(AZIONA_WORKSPACE, 'infrastructure')
}

RC = """
# AZIONA CONFIG (configured in %s)
source %s/.env
source ${NEULABS_ACTIVE_PERSISTENT_PATH:-}
export PATH=$PATH:$NEULABS_BIN_PATH
# AZIONA CONFIG END
""" % (datetime.datetime.now(), NEULABS_PATH)


def _configurations():
    try:
        os.makedirs(f"{ENV['NEULABS_WORKSPACE']}", exist_ok=True)
    except Exception as e:
        print(f"Error {ENV['NEULABS_WORKSPACE']} creation.")
        print(str(e))
        return 1

    os.makedirs(f"{ENV['NEULABS_PATH']}", exist_ok=True)
    os.makedirs(f"{ENV['NEULABS_TENANT_PATH']}", exist_ok=True)
    os.makedirs(f"{ENV['NEULABS_MODULES_PATH']}", exist_ok=True)
    os.makedirs(f"{ENV['NEULABS_BIN_PATH']}", exist_ok=True)
    os.makedirs(f"{ENV['AZIONA_TERRAFORM_MODULES_PATH']}", exist_ok=True)

    if os.path.isfile(ENV['NEULABS_ENV_PATH']) is True:
        os.rename(ENV['NEULABS_ENV_PATH'], str(
            ENV['NEULABS_ENV_PATH']) + '.old')

    with open(ENV['NEULABS_ENV_PATH'], 'w') as f:
        for key, value in ENV.items():
            f.write(f'export {key}={value}\n')

    with open(ENV['NEULABS_ACTIVE_PERSISTENT_PATH'], 'w') as f:
        f.write('')

    print('Check in .bashrc or/and .zshrc file: \n' + RC + '\n')

    bashrc_path = os.getenv('HOME') + '/.bashrc'
    if os.path.isfile(bashrc_path):
        with open(bashrc_path, 'r') as f:
            if 'AZIONA CONFIG' not in f.read():
                with open(bashrc_path, 'a') as f:
                    f.write(RC)

    zshrc_path = os.getenv('HOME') + '/.zshrc'
    if os.path.isfile(zshrc_path):
        with open(zshrc_path, 'r') as f:
            if 'AZIONA CONFIG' not in f.read():
                with open(zshrc_path, 'a') as f:
                    f.write(RC)


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
