PYTHON = python3

.PHONY: install run debug clean lint

install:
	$(PYTHON) -m pip install flake8 mypy

run:
	$(PYTHON) a_maze_ing.py config.txt

debug:
	$(PYTHON) -m pdb a_maze_ing.py config.txt

clean:
	rm -rf .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
