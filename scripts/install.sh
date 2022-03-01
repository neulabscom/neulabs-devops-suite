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
    
    make neulabs-env

    if [ -f ~/.bashrc ] ; then
        source ~/.bashrc
    fi

    if [ -f ~/.zshrc ] ; then
        source ~/.zshrc
    fi

    make neulabs-bin

    make neulabs-dependencies

    make apply
}

main "$@"