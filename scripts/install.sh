#!/bin/bash
set -eE -o functrace

failure() {
  local lineno=$1
  local msg=$2
  echo "Failed at $lineno: $msg"
}
trap 'failure ${LINENO} "$BASH_COMMAND"' ERR

set -o pipefail

main(){
    git clone https://github.com/neulabscom/neulabs-devops-suite.git /tmp/neulabs-devops-suite

    cd /tmp/neulabs-devops-suite
    
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