lint:
	PYTHONPATH=implementations/cursor-agent ruff check . --fix

format:
	PYTHONPATH=implementations/cursor-agent ruff format .

test:
	PYTHONPATH=implementations/cursor-agent pytest -q

check: lint test