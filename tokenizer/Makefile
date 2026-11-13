.PHONY: help install test coverage run

help:
	@echo "make install       - установить зависимости (uv sync)"
	@echo "make test          - запустить тесты"
	@echo "make coverage      - запустить тесты и показать покрытие"
	@echo "make run <файл>    - запустить токенизатор, например: make run input.txt"
	@echo "make help          - показать справку"

install:
	uv sync

test:
	uv run python -m pytest -v test_main.py

coverage:
	uv run python -m coverage run --source=main -m pytest -q test_main.py
	uv run python -m coverage report -m

ifeq ($(firstword $(MAKECMDGOALS)),run)
RUN_FILE := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
%:
	@:
endif

run:
	@test -n "$(RUN_FILE)" || { echo "Использование: make run <имя файла>"; exit 1; }
	uv run python main.py "$(RUN_FILE)"
