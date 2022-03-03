#!/usr/bin/env python3

import sys
import argparse
import os
import subprocess


def argsinstance(parser = None):
    def _ecr_login(parser):
        parser_ecr_login = parser.add_parser("ecr-login", help="Login to ECR repository")
        
        parser_ecr_login.add_argument(
            "--account-id",
            required=True,
            default=None,
            type=str,
            help="Account id ecr",
        )
        parser_ecr_login.add_argument(
            "--region",
            required=True,
            default=None,
            type=str,
            help="AWS region repository",
        )
        parser_ecr_login.add_argument(
            "--profile",
            required=False,
            default=None,
            type=str,
            help="AWS profile",
        )

    if parser is None:
        parser = argparse.ArgumentParser()
    
    subparsers = parser.add_subparsers(help="Help for command", dest="subcommand")
    _ecr_login(subparsers)

    return parser


def ecr_login_action(args):
    profile = "--profile " + args.profile if args.profile else ""
    command = f"aws {profile} ecr get-login-password --region {args.region} | docker login --username AWS --password-stdin {args.account_id}.dkr.ecr.{args.region}.amazonaws.com"

    subprocess.check_call(command, shell=True)

def main(args = None):
    try:
        if os.getenv("NEULABS_ENABLED") != "true":
            print("[ERROR] Before activate neulabs env with: neulabs-activate")
            return 1
        print(os.getenv("AZIONA_WELCOME_MESSAGE"))

        if args is None:
            args = argsinstance().parse_args()

        if args.subcommand == "ecr-login":
            ecr_login_action(args)
    except KeyboardInterrupt:
        return 0

if __name__ == "__main__":
    sys.exit(main())
