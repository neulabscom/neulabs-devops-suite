#!/bin/bash
set -eE -o functrace

delete_tmp_dir() {
  if [ -d ${TMP_DIRPATH} ] ; then
    rm -Rf ${TMP_DIRPATH}
  fi
}

failure() {
  local lineno=$1
  local msg=$2
  delete_tmp_dir
  echo "Failed at $lineno: $msg"
}
trap 'failure ${LINENO} "$BASH_COMMAND"' ERR

set -o pipefail

TMP_DIRPATH="/tmp/neulabs-devops-suite"

main(){
    delete_tmp_dir

    git clone https://github.com/neulabscom/neulabs-devops-suite.git ${TMP_DIRPATH}

    cd ${TMP_DIRPATH}
    
    chmod +x -R scripts bin
    python3 scripts/setup.py

    if [ -f ~/.bashrc ] ; then
        source ~/.bashrc
    fi

    if [ -f ~/.zshrc ] ; then
        source ~/.zshrc
    fi

    python3 scripts/bin.py --sync

    neulabs-dependencies

    neulabs-projects --yes --filename .projects-base.yml
}

main "$@"