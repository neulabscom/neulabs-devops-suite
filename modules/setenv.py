#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys

ACTIVATE_FILE = ''


def argsinstance(parser=None):
    if parser is None:
        parser = argparse.ArgumentParser()

    parser.add_argument(
        '-e',
        '--env',
        required=True,
        type=str,
        help='Env tenant',
    )
    parser.add_argument(
        '-c',
        '--company',
        required=True,
        type=str,
        help='Comapny name',
    )
    parser.add_argument(
        '--aws-role',
        required=False,
        default=None,
        type=str,
        help='AWS role',
    )
    parser.add_argument(
        '--aws-profile',
        required=False,
        default=None,
        type=str,
        help='AWS profile used as credential',
    )
    parser.add_argument(
        '--persistent-active',
        required=False,
        default=False,
        action='store_true',
        help='Active persistent env',
    )
    parser.add_argument(
        '--persistent-deactive',
        required=False,
        default=False,
        action='store_true',
        help='Deactive persistent env',
    )
    parser.add_argument(
        '--aws-serial-number',
        required='--aws-token-code' in sys.argv,
        default=None,
        type=str,
        help='Deactive persistent env',
    )
    parser.add_argument(
        '--aws-token-code',
        required='--aws-serial-number' in sys.argv,
        default=None,
        type=str,
        help='Deactive persistent env',
    )
    parser.add_argument(
        '--without-cert',
        default=False,
        action='store_true',
        help='Return only env vars',
    )
    return parser


def get_default_configpath(company):
    return pathlib.Path(os.getenv('NEULABS_TENANT_PATH'), company)


def write_activate_file(data):
    if not isinstance(data, str):
        raise Exception('Param data is not a string')
    global ACTIVATE_FILE
    ACTIVATE_FILE += data


def save_activate_file(path):
    with open(path, 'w') as f:
        f.write(ACTIVATE_FILE)


def add_export_to_activate_file(name, value, write_environ=True):
    write_activate_file(f"export {name}='{value}'\n")
    if write_environ:
        os.environ[name] = value


def aws_assume_role(role, account_id, profile=None, token_code=None, serial_number=None):
    add_export_to_activate_file('AWS_ROLE', role)
    add_export_to_activate_file('AWS_PROFILE', profile or '')

    profile = f'--profile {profile}' if profile else ''
    mfa = ''
    if token_code and serial_number:
        mfa = f'--serial-number {serial_number} --token-code {token_code}'

    command = f'aws {profile} sts assume-role {mfa} --role-arn arn:aws:iam::{account_id}:role/{role} --role-session-name {role}-cli'

    try:
        output = subprocess.check_output(command, shell=True)
        response = json.loads(output.decode().replace('\n', ''))
        add_export_to_activate_file(
            'AWS_ACCESS_KEY_ID', response['Credentials']['AccessKeyId'])
        add_export_to_activate_file(
            'AWS_SESSION_TOKEN', response['Credentials']['SessionToken'])
        add_export_to_activate_file(
            'AWS_SECRET_ACCESS_KEY', response['Credentials']['SecretAccessKey'])
    except subprocess.CalledProcessError as e:
        raise e


def create_kube_cert(cluster, region, kubeconfig_path, profile=None):
    profile = f'--profile {profile}' if profile else ''
    p = subprocess.run(f'eksctl utils write-kubeconfig {profile} --cluster {cluster} --region {region} --kubeconfig {kubeconfig_path}',
                       stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    if p.returncode != 0:
        raise Exception(p.stderr.decode())


def persistent_deactivate():
    path = os.getenv('NEULABS_ACTIVE_PERSISTENT_PATH')
    with open(path, 'w') as f:
        f.write('')
    return 0


def persistent_activate():
    persistent_deactivate()
    return os.getenv('NEULABS_ACTIVE_PERSISTENT_PATH')


def activate():
    persistent_deactivate()

    path = os.getenv('NEULABS_ACTIVE_PATH')
    if os.path.isfile(path):
        os.remove(path)

    return path


def default_env_vars(company, env, config_path):
    add_export_to_activate_file('NEULABS_ENABLED', 'true')
    add_export_to_activate_file(
        'CONFIG_TENANT_SETTINGS_PATH', str(config_path))
    add_export_to_activate_file('KUBECONFIG', str(pathlib.Path(os.getenv(
        'HOME'), '.kube/eksctl/clusters', os.getenv('EKS_CLUSTER_NAME', ''))))
    add_export_to_activate_file('AZIONA_WELCOME_MESSAGE', f"""
****
*
* Welcome into Neulabs env
*
****
*
* Comany: {company}
* Env: {env}
*
****
""")


def main(args=None):
    try:
        if args is None:
            args = argsinstance().parse_args()

        config_path = get_default_configpath(args.company)

        if args.persistent_deactive:
            return persistent_deactivate()

        if args.persistent_active:
            active_path = persistent_activate()
        else:
            active_path = activate()

        if os.path.isdir(config_path) is False:
            print('Tenant directory not found: ' + config_path)
            print('Download tenant settings')
            git_tenant_url = input('Input git repository url: ')
            subprocess.check_call(
                f'git clone {git_tenant_url} {config_path}', shell=True)

        # file .env tenant
        tenant_path = pathlib.Path(config_path, args.env, '.env')
        if os.path.isfile(tenant_path) is False:
            raise Exception('Tenant file not exist: ' + tenant_path)

        # import f  ile .env in os and to ACTIVATE_FILE var
        with open(tenant_path, 'r') as f:
            for line in f.read().split('\n'):
                if line.startswith('#') or line == '':
                    continue
                name, value = line.split('=')
                add_export_to_activate_file(name, value)

        default_env_vars(config_path, args.env, config_path)

        if args.aws_role:
            aws_assume_role(
                role=args.aws_role,
                account_id=os.getenv('ACCOUNT_ID'),
                profile=args.aws_profile,
                token_code=args.aws_token_code,
                serial_number=args.aws_serial_number
            )

        if args.without_cert is False:
            create_kube_cert(
                cluster=os.getenv('EKS_CLUSTER_NAME'),
                region=os.getenv('EKS_AWS_REGION'),
                kubeconfig_path=os.getenv('KUBECONFIG'),
                profile=args.aws_profile
            )

        write_activate_file(f"echo 'Aziona - env active: {args.env}'\n")

        save_activate_file(active_path)
    except KeyboardInterrupt as e:
        raise Exception(str(e))
    except Exception as e:
        raise Exception(str(e))
    else:
        return 0


if __name__ == '__main__':
    sys.exit(main())
