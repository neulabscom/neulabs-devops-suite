# Neulabs - DevOps

### Requirments


1. Python >= 3.8 \[[install](https://www.python.org/downloads/)\]
    - With: pip3, python3-venv
2. Nodjs >= 14.19 \[[install](https://github.com/nvm-sh/nvm)\]
3. VSCode \[[install](https://code.visualstudio.com/download)\]
4. Utils:
    - bash
    - curl
5. Only MacOS
    - Docker \[[install](https://docs.docker.com/desktop/mac/install/)\]
    - Homebrew

### Get Started

    curl -o- https://raw.githubusercontent.com/neulabscom/neulabs-devops-suite/main/install.sh | bash

    neulabs system dependencies-install

    gh auth login

    neulabs workspace add --workspace azionaventures --name aziona-cli --url git@github.com:azionaventures/aziona-cli.git
    neulabs workspace add --workspace azionaventures --name infrastructure --url git@github.com:azionaventures/infrastructure.git
    neulabs workspace add --workspace neulabs --name neulabs-devops-suite --url git@github.com:azionaventures/neulabs-devops-suite.git

### Usage

... in progress

### Devmode

    git clone https://github.com/neulabscom/neulabs-devops-suite.git
    cd neulabs-devops-suite
    make develop
    source .activate
