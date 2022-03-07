.PHONY: help

help: ## helper
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.DEFAULT_GOAL := help

_chmod:
	chmod -R +x ./scripts ./bin ./*.sh

develop: _chmod
	./develop.sh

lint:
	pre-commit run --all-files
