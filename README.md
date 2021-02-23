# altagram

[![Build Status](https://travis-ci.com/myslak71/altagram.svg?branch=master)](https://travis-ci.com/myslak71/altagram)

### Requirements
- Docker 20.10.3
- docker-compose 1.27.4

### Run
The application can run by using `make up` command, and the endpoint is available at:
[localhost:8000/starships/](localhost:8000/starships/). The application start can take a couple of minutes because of
starship crawling - be patient then! :)

REST API documentation is served alongside the application and is available at 
[localhost:8000/docs](localhost:8000/docs).

### Testing
Tests with coverage can be run with `make run-tests` command.

### Linting
Linters can be run with `make lint` command.

