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

**Start shell with company credentials**:

    # Start env in terminal
    source aziona-activate --company NOME --env ENV

    - or - 

    # Start env persistent
    source aziona-persistent-activate --company NOME --env ENV

**De-active persistent env**:

    source aziona-persistent-deactivate


**Manager add/update terraform, bin, and tenant-settings**:

    aziona-manager --help


**Enter in container on specific POD**:

    aziona-kube-exec -p POD_NAME -c CONTAINER_NAME

**Login to aws-ecr**:

    aziona-ecr-login

**Run infrastructure templates**:

    aziona-infra -t TEMPLATE_NAME target1 target2 ...

