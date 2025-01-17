PYTHON := python3
SCRIPT := src/main.py
TEST_DIR := tests
TEST_DIR_BNB := tests/adapted_tests

run:
	$(PYTHON) $(SCRIPT) $(ALG) $(TEST_DIR)/$(TEST)

test_tat:
	@for test_file in $(TESTE_DIR)/*.tsp; do \
		echo "Executando teste: $$test_file"; \
		$(PYTHON) $(SCRIPT) TAT "$$test_file"; \
	done

test_c:
	@for test_file in $(TESTE_DIR)/*.tsp; do \
		echo "Executando teste: $$test_file"; \
		$(PYTHON) $(SCRIPT) C "$$test_file"; \
	done

test_bnb:
	@for test_file in $(TESTE_DIR)/*.tsp; do \
		echo "Executando teste: $$test_file"; \
		$(PYTHON) $(SCRIPT) BNB "$$test_file"; \
	done

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +
	rm -f results.txt
