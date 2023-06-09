# Inspired by https://postd.cc/auto-documented-makefile/
MAKEFLAGS += --warn-undefined-variables
SHELL = /bin/bash
.SHELLFLAGS = -e -o pipefail -c
.DEFAULT_GOAL = help

# Use UTF-8 as Python default encoding
export PYTHONUTF8 = 1

# If SHLVL is undefined, use bash in "Git for Windows"
ifndef SHLVL
    SHELL = C:\Program Files\Git\bin\bash.exe
endif

# Make all targets PHONY other than targets including . in its name
.PHONY: $(shell grep -oE ^[a-zA-Z0-9%_-]+: $(MAKEFILE_LIST) | sed 's/://')

# Variables
POETRY = poetry
PRE_COMMIT = $(POETRY) run pre-commit

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9%_-]+:.*?## / {printf "    \033[36m%-16s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Configure a local dev environment. Execute once after cloning this repository
	poetry self add "poetry-dynamic-versioning[plugin]"
	$(POETRY) install
	$(PRE_COMMIT) install
	$(PRE_COMMIT) install-hooks

lint: ## Lint all files
	$(PRE_COMMIT) run --all-files

pre-commit-%: ## Run a specific pre-commit hook
	$(PRE_COMMIT) run --all-files $*

lint-no-reviewdog: ## Lint by linters which is not used with reviewdog in CI
	@comm -23 <(yq '.repos[].hooks[].id' .pre-commit-config.yaml | sort) \
	    <(echo black flake8 isort mypy no-commit-to-branch | tr " " "\n") | xargs -L 1 $(PRE_COMMIT) run --all-files

test: ## Test by pytest
	$(POETRY) run pytest .

PYINSTALLER = pyinstaller
PYINSTALLER_FLAGS = --onefile
UNAME := $(shell uname -s)
ifeq ($(UNAME), Linux)
	PYINSTALLER_FLAGS += --strip
endif
build-exe: ## Build a single executable by pyinstaller
	$(PYINSTALLER) ./bin/aws-clipper.py $(PYINSTALLER_FLAGS)

EXECUTABLE_NAME = aws-clipper
UPLOAD_NAME = aws-clipper-$(EXECUTABLE_SUFFIX)
ifeq ($(OS), Windows_NT)
	EXECUTABLE_NAME = aws-clipper.exe
	UPLOAD_NAME = aws-clipper-$(EXECUTABLE_SUFFIX).exe
endif
upload-exe: ## Upload a single executable to GitHub release assets
# Rename executable
	mv dist/$(EXECUTABLE_NAME) dist/$(UPLOAD_NAME)
	gh release upload $(TAG_NAME) dist/$(UPLOAD_NAME) $(UPLOAD_FLAGS)
