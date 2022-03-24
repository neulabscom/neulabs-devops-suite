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
  python3 -m venv .venv

  # shellcheck disable=SC1091
  source .venv/bin/activate

  pip install -r requirements-dev.txt
  pip install -r requirements.txt
  pre-commit install
}

main "$@"
