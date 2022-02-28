.PHONY: help

help: ## helper
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.DEFAULT_GOAL := help

_chmod:
	chmod +x scripts bin

setenv:
	python3 scripts/setenv.py

bin:
	python3 scripts/bin.py

dependencies:
	python3 scripts/dependencies.py

apply:
	python3 scripts/apply.py

setup: _chmod setenv 

