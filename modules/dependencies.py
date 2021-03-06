#!/usr/bin/env python3
from __future__ import annotations

import argparse
import platform
import subprocess
import sys
from shutil import which

from distutils.version import LooseVersion

DEPS = {
    'git': {
        'version': None,
        'install': {
            'ubuntu': ('sudo apt-get install -y git',),
            'darwin': ('brew install git', ),
        }
    },
    'make': {
        'version': None,
        'install': {
            'ubuntu': ('sudo apt-get install -y make',),
            'darwin': ('brew install make', ),
        }
    },
    'docker': {
        'version': None,
        'install': {
            'ubuntu': (
                'sudo apt-get update',
                'sudo apt-get install ca-certificates gnupg lsb-release',
                'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -',
                'sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"',
                'sudo apt-get update',
                'sudo apt-get install -y docker-ce docker-ce-cli containerd.io'
            ),
            'darwin': (),
        }
    },
    'tfenv': {
        'version': None,
        'install': {
            'ubuntu': (
                'git clone https://github.com/tfutils/tfenv.git ~/.tfenv',
                'sudo ln -s ~/.tfenv/bin/* /usr/local/bin'
            ),
            'darwin': (
                'brew install tfenv',
            ),
        },

    },
    'terraform': {
        'version': LooseVersion('1.1.7'),
        'install': {
            'ubuntu': (
                'tfenv terraform %version%',
                'tfenv use %version%'
            ),
            'darwin': (
                'tfenv terraform %version%',
                'tfenv use %version%'
            ),
        },
    },
    'kubectl': {
        'version': LooseVersion('1.23.0'),
        'install': {
            'ubuntu': (
                'curl -LO https://storage.googleapis.com/kubernetes-release/release/v%version%/bin/linux/amd64/kubectl',
                'chmod +x ./kubectl',
                'sudo mv ./kubectl /usr/local/bin/kubectl',
                'pip3 install kubernetes'
            ),
            'darwin': (
                'brew install kubectl@%version%',
                'pip3 install kubernetes'
            ),
        },
    },
    'eksctl': {
        'version': LooseVersion('0.97.0'),
        'install': {
            'ubuntu': (
                'curl --location https://github.com/weaveworks/eksctl/releases/download/v%version%/eksctl_$(uname -s)_$(dpkg --print-architecture).tar.gz | tar xz -C /tmp',
                'sudo mv /tmp/eksctl /usr/local/bin',
            ),
            'darwin': (
                'curl --location https://github.com/weaveworks/eksctl/releases/download/v%version%/eksctl_$(uname -s)_$(uname -m).tar.gz | tar xz -C /tmp',
                'sudo mv /tmp/eksctl /usr/local/bin',
            ),
        },
    },
    'kustomize': {
        'version': LooseVersion('4.0.5'),
        'install': {
            'ubuntu': (
                'curl -s https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh  | bash',
                'sudo mv ./kustomize /usr/local/bin'
            ),
            'darwin': ('brew install kustomize',),
        },
    },
    'aws': {
        'version': LooseVersion('2'),
        'install': {
            'ubuntu': (
                'cd /tmp'
                'curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"',
                'unzip awscliv2.zip',
                'sudo ./aws/install',
                'rm ./aws/install'
            ),
            'darwin': (
                'curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"',
                'sudo installer -pkg AWSCLIV2.pkg -target /'
            ),
        },
    },
    'aws-iam-authenticator': {
        'version': LooseVersion('1.19.6'),
        'install': {
            'ubuntu': (
                'curl -O https://amazon-eks.s3.us-west-2.amazonaws.com/%version%/2021-01-05/bin/linux/amd64/aws-iam-authenticator',
                'chmod +x ./aws-iam-authenticator',
                'sudo mv ./aws-iam-authenticator /usr/local/bin',
            ),
            'darwin': ('brew install aws-iam-authenticator',),
        },
    },
    'aziona': {
        'version': LooseVersion('0.1'),
        'install': {
            'ubuntu': ('pip3 install aziona==%version%',),
            'darwin': ('pip3 install aziona==%version%',),
        },
    },
    'gh': {
        'version': None,
        'install': {
            'ubuntu': (
                'curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg',
                'echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null',
                'sudo apt update',
                'sudo apt-get install -y gh',
            ),
            'darwin': ('brew install gh', ),
        }
    },
    'jq': {
        'version': None,
        'install': {
            'ubuntu': ('sudo apt-get install -y jq',),
            'darwin': ('brew install jq', ),
        }
    }
}


def argsinstance(parser=None):
    if parser is None:
        parser = argparse.ArgumentParser()

    parser.add_argument(
        '-y', '--yes',
        action='store_true',
        default=False,
        help='Accept request intput',
    )
    parser.add_argument(
        '-f', '--force',
        action='store_true',
        default=False,
        help='Force install packages',
    )
    parser.add_argument(
        '--skip',
        nargs='+',
        default=[],
        help='Skip packages',
    )
    return parser


def deps_exist(name: str):
    return which(name) is not None


def linux(args):
    def get_distribution():
        import csv

        dist = {}
        with open('/etc/os-release') as f:
            reader = csv.reader(f, delimiter='=')
            for row in reader:
                if row:
                    dist[row[0]] = row[1]

        print('Distribution: %s' % dist.get('NAME', '').lower())
        print('Release: %s' % dist.get('VERSION_ID', '').lower())
        print('Version: %s' % dist.get('VERSION', '').lower())
        return dist['NAME'].lower()

    dist = get_distribution()

    distro = "ubuntu" if dist.lower() == 'pop!_os' else dist.lower()
    
    if 'ubuntu' not in distro:
        raise RuntimeError('Distribution not supported. Use MacOS or Ubuntu')

    exec(distro=distro, force_install=args.force, skip=args.skip)


def darwin(args):
    exec(distro='darwin', force_install=args.force, skip=args.skip)


def exec(distro: str, force_install: bool = False, skip: list = []):
    if distro not in ('darwin', 'ubuntu', 'alpine'):
        raise RuntimeError('Not found scripts for yor os distribution')

    for key, data in DEPS.items():
        if deps_exist(key) and force_install is False:
            print(f"\n{key} installed.\nSuggestion version {data['version']}")
            continue

        if key in skip:
            print(f'{key} installation skipped')
            continue

        print(f'+ Package: {key}')
        print(f"  Version: {data['version']}")

        for cmd in data['install'].get(distro, []):
            if data['version']:
                cmd = cmd.replace('%version%', str(data['version']))

            try:
                subprocess.check_call(cmd, shell=True)
            except Exception as e:
                print(str(e))
                print('\n!!! Report error to DevOps\n')
                sys.exit(1)


def main(args=None):
    try:
        if args is None:
            args = argsinstance().parse_args()

        if platform.system() == 'Linux':
            linux(args)

        if platform.system() == 'Darwin':
            darwin(args)

        if platform.system() == 'Windows':
            raise RuntimeError(
                'Distribution not supported. Use MacOS or Ubuntu')
    except KeyboardInterrupt:
        return 0


if __name__ == '__main__':
    sys.exit(main())
