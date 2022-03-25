#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys
from ctypes import ArgumentError

import yaml

AZIONA_PATH = os.getenv('AZIONA_PATH', None)
if not AZIONA_PATH:
    raise Exception('AZIONA_PATH not found in env. Configure neulabs env')

NEULABS_PATH = os.getenv('NEULABS_PATH', None)
if not NEULABS_PATH:
    raise Exception('NEULABS_PATH not found in env. Configure neulabs env')

NEULABS_WORKSPACE = os.getenv('NEULABS_WORKSPACE', None)
if not NEULABS_WORKSPACE:
    raise Exception(
        'NEULABS_WORKSPACE not found in env. Configure neulabs env')

# WORKSPACE VARS
WS_CONFIGURATION_FILEPATH = pathlib.Path(NEULABS_PATH, '.projects.yml')
WS_EXCLUDE = ('projects.code-workspace', '.vscode')


def argsinstance(parser=None):
    def _add(parser):
        parser_add = parser.add_parser('add', help='Add project')
        parser_add.add_argument(
            '-n',
            '--name',
            required=True,
            type=str,
            help='Project name',
        )
        parser_add.add_argument(
            '-u',
            '--url',
            required=True,
            type=str,
            help='Repository url',
        )
        parser_add.add_argument(
            '-w',
            '--workspace',
            required=True,
            type=str,
            help='Workspace name',
        )

    def _update(parser):
        parser_update = parser.add_parser('update', help='Update project')
        parser_update.add_argument(
            '-n',
            '--name',
            required=True,
            type=str,
            help='Project name',
        )
        parser_update.add_argument(
            '-u',
            '--url',
            required=True,
            type=str,
            help='Repository url',
        )
        parser_update.add_argument(
            '-w',
            '--workspace',
            required=True,
            type=str,
            help='Workspace name',
        )

    def _remove(parser):
        parser_remove = parser.add_parser('remove', help='Remove project')
        parser_remove.add_argument(
            '-n',
            '--name',
            required=True,
            type=str,
            help='Project name',
        )
        parser_remove.add_argument(
            '-w',
            '--workspace',
            required=True,
            type=str,
            help='Workspace name',
        )

    if parser is None:
        parser = argparse.ArgumentParser()

    parser.add_argument(
        '--force',
        action='store_true',
        default=False,
        help='Force yes to answer',
    )

    subparsers = parser.add_subparsers(
        help='Help for command', dest='subcommand')

    _add(subparsers)
    _update(subparsers)
    _remove(subparsers)

    return parser


def get_workspace_projects(path):
    if not os.path.isdir(path):
        return []
    return [w for w in os.listdir(path) if w not in WS_EXCLUDE]


def confirm(yes: bool = False) -> bool:
    if yes is False and input('Do you want to proceed with the indicated changes? [y/n] ').lower() not in ('y', 'yes'):
        return False
    return True


def add_project(workspace, project, url, force):
    workspace_path = pathlib.Path(NEULABS_WORKSPACE, workspace)
    project_path = pathlib.Path(workspace_path, project)

    if project in get_workspace_projects(workspace_path):
        print(f'[ERROR] {project} exist: {project_path}')
        return

    if not confirm(force):
        return

    cmd = f'git clone {url} {project_path}'
    subprocess.check_call(cmd, shell=True)
    print(f'[SUCCESS] Add {project} in {project_path}')

    create_vscode_workspace(workspace, project)


def remove_workspace(workspace):
    workspace_path = pathlib.Path(NEULABS_WORKSPACE, workspace)

    if os.path.isdir(workspace_path):
        subprocess.check_call(f'rm -rf {workspace_path}', shell=True)
        print(f'[SUCCESS] Remove workspace {workspace}: {workspace_path}')
    else:
        print(f'[ERROR] Remove {workspace}: {workspace_path}')


def remove_project(workspace, project, force):
    workspace_path = pathlib.Path(NEULABS_WORKSPACE, workspace)
    project_path = pathlib.Path(workspace_path, project)

    if project not in get_workspace_projects(workspace_path):
        print(f'[ERROR] Project {project} not exist {project_path}')
        return

    if not confirm(force):
        return

    subprocess.check_call(f'rm -rf {project_path}', shell=True)
    print(f'[SUCCESS] Remove project {project} in {project_path}')

    if not get_workspace_projects(workspace_path):
        remove_workspace(workspace=workspace)


def create_vscode_workspace(workspace, project):
    workspace_filepath = pathlib.Path(
        NEULABS_WORKSPACE, workspace, 'projects.code-workspace')

    if os.path.isfile(str(workspace_filepath)):
        with open(str(workspace_filepath), 'r') as f:
            vs_workspace = json.loads(f.read())
    else:
        vs_workspace = {
            'folders': [],
            'settings': {}
        }

    vs_workspace['folders'].append({
        'name': project,
        'path': str(pathlib.Path(NEULABS_WORKSPACE, workspace, project))
    })

    with open(str(workspace_filepath), 'w') as f:
        f.write(json.dumps(vs_workspace))


def main(args=None):  # noqa: C901
    try:
        if args is None:
            args = argsinstance().parse_args()

        if not isinstance(args, argparse.Namespace):
            raise Exception('args not valid')

        if args.subcommand == 'add':
            print('[ADD CHANGES]')
            print(f' - Workspace: {args.workspace}')
            print(f' - Name: {args.name}')
            print(f' - Url: {args.url}')
            add_project(workspace=args.workspace, project=args.name,
                        url=args.url, force=args.force)

        if args.subcommand == 'remove':
            print('[REMOVE CHANGES]')
            print(f' - Workspace: {args.workspace}')
            print(f' - Name: {args.name}')
            remove_project(workspace=args.workspace,
                           project=args.name, force=args.force)

        if args.subcommand == 'update':
            print('[UPDATE CHANGES]')
            print(f' - Workspace: {args.workspace}')
            print(f' - Name: {args.name}')
            print(f' - Url: {args.url}')
            remove_project(workspace=args.workspace,
                           project=args.name, force=args.force)
            add_project(workspace=args.workspace, project=args.name,
                        url=args.url, force=args.force)

    except KeyboardInterrupt as e:
        raise Exception(str(e))
    except Exception as e:
        raise Exception(str(e))
    else:
        return 0


if __name__ == '__main__':
    sys.exit(main())
