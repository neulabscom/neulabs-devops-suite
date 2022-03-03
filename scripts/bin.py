#!/usr/bin/env python3

import argparse
import sys
import os
import pathlib
import shutil

def argsinstance():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sync",
        action="store_true",
        default=False,
        help="Sync bin folder",
    )
    return parser

def _scripts(args):
    dest_dir = os.getenv("NEULABS_BIN_PATH", pathlib.Path(os.getenv("HOME"), ".neulabs", "bin"))
    if not os.path.isdir(dest_dir):
        print(f"NEULABS_BIN_PATH not found in {dest_dir}")
        return 1

    if args.sync:
        print("Sync bin folder")
        for file_name in os.listdir(dest_dir):
            path = pathlib.Path(dest_dir, file_name)
            if os.path.isdir(path):
                shutil.rmtree(path)
            if os.path.isfile(path):
                os.remove(path)
            print(f"Remove {path}")
        
    source_dir = pathlib.Path(pathlib.Path(__file__).parent.resolve(), "..", "bin") 
    for file_name in os.listdir(source_dir):
        source = pathlib.Path(source_dir, file_name)
        destination = pathlib.Path(dest_dir, file_name)
        if os.path.isfile(source):
            shutil.copy(source, destination)
            print(f"Copied {file_name} in {destination}")

def main():
    try:
        args = argsinstance().parse_args()
        _scripts(args)
    except KeyboardInterrupt as e:
        pass

if __name__ == "__main__":
    sys.exit(main())
