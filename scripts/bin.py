#!/usr/bin/env python3

import sys
import os
import pathlib

def _scripts():
    import shutil

    dest_dir = os.getenv("NEULABS_BIN_PATH", pathlib.Path(os.getenv("HOME"), ".neulabs", "bin"))
    if not os.path.isdir(dest_dir):
        print(f"NEULABS_BIN_PATH not found in {dest_dir}")
        return 1

    source_dir = pathlib.Path(pathlib.Path(__file__).parent.resolve(), "..", "bin") 
    
    for file_name in os.listdir(source_dir):
        source = pathlib.Path(source_dir, file_name)
        destination = pathlib.Path(dest_dir, file_name)
        if os.path.isfile(source):
            shutil.copy(source, destination)
            print(f"Copied {file_name} in {destination}")

def main():
    try:
        _scripts()
    except KeyboardInterrupt as e:
        pass

if __name__ == "__main__":
    sys.exit(main())
