#!/usr/bin/env python3

import pathlib
import sys
import argparse
import os
import subprocess


def argsinstance(parser = None):    
    if parser is None:
        parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "-t",
        "--template",
        required=True,
        type=str,
        help="Name of infrastructure template",
    )
    parser.add_argument(
        "--template-path",
        required=False,
        default=os.getenv("PROJECT_INFRASTRUCTURE"),
        type=str,
        help="Basepath of templates",
    )
    parser.add_argument(
        'targets', 
        metavar='targets', 
        type=str, 
        nargs='+',
        help="Target name")
    return parser

def main(args = None):
    try:
        if os.getenv("NEULABS_ENABLED") != "true":
            print("[ERROR] Before activate neulabs env with: neulabs-activate")
            return 1
        print(os.getenv("AZIONA_WELCOME_MESSAGE"))

        if args is None:
            args = argsinstance().parse_args()

        template = pathlib.Path(args.template_path, "template", f"{args.template}.yml")

        command = f"aziona -v -f {template} " + " ".join(args.targets)

        subprocess.check_call(command, shell=True)
    except KeyboardInterrupt:
        return 0

if __name__ == "__main__":
    sys.exit(main())
