SHELL = /bin/bash
.PHONY: help

_UID	:= $(shell id -u)
_GID	:= $(shell id -g)

_MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
_CURRENT_PATH := $(dir $(_MKFILE_PATH))

_DOCS_RUN := docker run -v "/$(_CURRENT_PATH)/docs":/docs altagram-docs
_LINT_RUN := docker run --rm altagram-lint
_TESTS_RUN := docker-compose -f docker/docker-compose-files/docker-compose-tests.yaml --project-directory ./ run --rm altagram-test

build-docs: ## Build docs docker image
	docker build -f docker/dockerfiles/Dockerfile-docs docs/ -t altagram-docs
	$(_DOCS_RUN) swagger-merger -i index.yml -o open_api.yml
	$(_DOCS_RUN) redoc-cli bundle open_api.yml -o api_docs.html

up: build-docs
	docker-compose -p altagram -f docker/docker-compose-files/docker-compose.yaml --project-directory  ./ up --build --renew

run-tests:
	docker-compose -f docker/docker-compose-files/docker-compose-tests.yaml --project-directory ./ build
	$(_TESTS_RUN) pytest tests/unit -s -vv --cov --cov-report term-missing
	$(_TESTS_RUN) pytest tests/integration -s -vv --cov --cov-report term-missing --cov-append
	docker-compose -f docker/docker-compose-files/docker-compose-tests.yaml --project-directory ./ down

lint: ## Run all linters
	docker build . -f docker/dockerfiles/Dockerfile-lint -t altagram-lint
	$(_LINT_RUN) black . --check
	$(_LINT_RUN) isort . --check
	$(_LINT_RUN) flake8
	$(_LINT_RUN) mypy .
	$(_LINT_RUN) safety check -r requirements.txt -r requirements-lint.txt \
				  -r requirements-test.txt
