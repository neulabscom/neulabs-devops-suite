#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import pathlib
import shutil
import sys


def argsinstance():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--sync',
        action='store_true',
        default=False,
        help='Sync bin folder',
    )
    return parser


def rsync(dirpath):
    print('Sync folder')
    for file_name in os.listdir(dirpath):
        path = pathlib.Path(dirpath, file_name)
        if os.path.isdir(path):
            shutil.rmtree(path)
        if os.path.isfile(path):
            os.remove(path)
        print(f'Remove {path}')


def copy(source_dirpath, dest_dirpath):
    for file_name in os.listdir(source_dirpath):
        source = pathlib.Path(source_dirpath, file_name)
        destination = pathlib.Path(dest_dirpath, file_name)
        if os.path.isfile(source):
            shutil.copy(source, destination)
            print(f'Copied {file_name} in {destination}')


def exec(dest_dirpath, source_dirpath, sync=False):
    if not os.path.isdir(dest_dirpath):
        raise Exception(f'{dest_dirpath} not found')

    if sync:
        rsync(dest_dirpath)

    copy(source_dirpath=source_dirpath, dest_dirpath=dest_dirpath)


def main():
    try:
        args = argsinstance().parse_args()
        exec(
            dest_dirpath=os.getenv('NEULABS_MODULES_PATH', pathlib.Path(
                os.getenv('HOME'), '.neulabs', 'modules')),
            source_dirpath=pathlib.Path(pathlib.Path(
                __file__).parent.resolve(), '..', 'modules'),
            sync=args.sync
        )
        exec(
            dest_dirpath=os.getenv('NEULABS_BIN_PATH', pathlib.Path(
                os.getenv('HOME'), '.neulabs', 'bin')),
            source_dirpath=pathlib.Path(pathlib.Path(
                __file__).parent.resolve(), '..', 'bin'),
            sync=args.sync
        )
    except KeyboardInterrupt:
        return 0


if __name__ == '__main__':
    sys.exit(main())
