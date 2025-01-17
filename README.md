# TSP_EUC_2D

 Algoritmos para solucionar o problema do caixeiro viajante, mais especificamente uma variação do problema na qual as entradas são euclidianas bidimensionais. 
 
## Como utilizar

- **`make run`**: Executa `src/main.py` com:
  - `ALG`: Algoritmo (`TAT`, `C`, `BNB`).
  - `TEST`: Arquivo de teste específico em `tests/`.

  Exemplo: `make run ALG=TAT TEST=example.tsp`

- **`make test_tat`**, **`make test_c`**, **`make test_bnb`**:
  Executam pilha de testes dos diretório `tests` (TSPLIB) ou `tests/adapted_tests` usando os algoritmos `Twice Around The Tree`, `Christophies` ou `Branch and Bound`.

- **`make clean`**: Remove arquivos temporários (`__pycache__`, `results.txt`).
