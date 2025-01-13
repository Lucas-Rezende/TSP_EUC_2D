PYTHON := python3
SCRIPT := src/main.py
TEST_DIR := tests

run:
	$(PYTHON) $(SCRIPT) $(ALG) $(TEST_DIR)/$(TEST)

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +