# Neulabs - DevOps

### Requirments


1. Python >= 3.8 \[[install](https://www.python.org/downloads/)\]
    - With: pip3, python3-venv
2. Nodjs >= 14.19 \[[install](https://github.com/nvm-sh/nvm)\]
3. VSCode \[[install](https://code.visualstudio.com/download)\]
4. Utils:
    - bash
    - curl
5. (Only MacOS) Docker \[[install](https://docs.docker.com/desktop/mac/install/)\]

### Get Started

Setup local env

    curl -o- https://raw.githubusercontent.com/neulabscom/neulabs-devops-suite/main/install.sh | bash

    gh auth login

    mkdir ~/.aws && touch ~/.aws/credentials

    ssh-keygen -t rsa -b 4096 -o -a 100 # (optional)


### Usage

... in progress

### Devmode

    git clone https://github.com/neulabscom/neulabs-devops-suite.git
    cd neulabs-devops-suite
    make develop
    source .activate
