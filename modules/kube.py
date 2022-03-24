#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys

from kubernetes import client
from kubernetes import config


def argsinstance(parser=None):
    def _exec(parser):
        parser_exec = parser.add_parser('exec', help='Kube exec')
        parser_exec.add_argument(
            '-p',
            '--pod',
            required=True,
            type=str,
            help='Pod name',
        )
        parser_exec.add_argument(
            '-c',
            '--container',
            type=str,
            help='Container name'
        )
        parser_exec.add_argument(
            '--cmd',
            default='/bin/bash',
            type=str,
            help='Comand'
        )

    if parser is None:
        parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(
        help='Help for command', dest='subcommand')
    _exec(subparsers)

    return parser


def exec_action(args):
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        ret = v1.list_pod_for_all_namespaces(watch=False)
    except config.config_exception.ConfigException as e:
        print(e)
        return 1
    except client.exceptions.ApiException as e:
        print(e)
        return 1

    pods = []
    pod_containers = {}
    index = 0
    for p in ret.items:
        if p.metadata.name.startswith(args.pod):
            containers = []
            for c in p.metadata.managed_fields[0].fields_v1.get('f:spec', {}).get('f:containers', {}).keys():
                containers.append(c.split(':')[2][1:-2])
            pods.append(p.metadata.name)
            pod_containers[index] = containers

            print(f'{index})\tPod: {p.metadata.name} \n\tContainer: {containers}\n')

            index += 1
    del containers

    index = int(input('Enter the index of the Pod: '))
    if index > len(pods):
        print(f'Index {index} not found')
        return 1

    container = args.container if args.container else input('Container name: ')
    if container not in pod_containers[index]:
        print(f'Container {container} not found in pod')
        return 1

    subprocess.check_call(
        f'kubectl exec -it {pods[index]} -c {container} -- {args.cmd}', shell=True)


def main(args=None):
    try:
        if os.getenv('NEULABS_ENABLED') != 'true':
            print('[ERROR] Before activate neulabs env with: neulabs-activate')
            return 1
        print(os.getenv('AZIONA_WELCOME_MESSAGE'))

        if args is None:
            args = argsinstance().parse_args()

        if args.subcommand == 'exec':
            exec_action(args)
    except KeyboardInterrupt:
        return 0


if __name__ == '__main__':
    sys.exit(main())
