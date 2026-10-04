.PHONY: help install run test coverage clean

help:
	@echo "make install   - установить зависимости (uv sync)"
	@echo "make run       - запустить калькулятор постфиксной нотации"
	@echo "make test      - запустить тесты (подробный вывод)"
	@echo "make coverage  - запустить тесты и показать покрытие"
	@echo "make clean     - удалить временные файлы"

install:
	uv sync

run:
	uv run python stack_mashine/main.py

test:
	uv run pytest tests -v

coverage:
	uv run coverage run --source=stack_mashine -m pytest tests -q
	uv run coverage report -m

clean:
	rm -rf .pytest_cache .coverage
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
