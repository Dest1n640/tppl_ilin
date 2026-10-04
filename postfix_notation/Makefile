# Выражения из задания
EXAMPLES = "3 0 4 ~ 2 ~" "2 2 + 4 - 4 ~ 2 3 * +"

help:
	@echo "make install       - установить зависимости (uv sync)"
	@echo "make run-examples  - запустить выражения из задания"
	@echo "make run <выражение> - вычислить своё выражение, например: make run \"3 4 + 2 *\""
	@echo "make test          - запустить тесты (подробный вывод)"
	@echo "make coverage      - запустить тесты и показать покрытие"
	@echo "make clean         - удалить временные файлы"

install:
	uv sync

run-examples:
	@for expr in $(EXAMPLES); do \
		echo "== $$expr"; \
		uv run python stack_mashine/main.py "$$expr"; \
	done

ifeq ($(firstword $(MAKECMDGOALS)),run)
RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
%:
	@:
endif

run:
	@test -n "$(RUN_ARGS)" || { echo 'Использование: make run "<выражение>"'; exit 1; }
	@uv run python stack_mashine/main.py $(foreach arg,$(RUN_ARGS),'$(arg)')

test:
	uv run pytest tests -v

coverage:
	uv run coverage run --source=stack_mashine -m pytest tests -q
	uv run coverage report -m

clean:
	rm -rf .pytest_cache .coverage
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
