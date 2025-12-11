# Mapeador-de-Conectividade
Repositório para um mapeador simples de conectividade de pontos (nós em uma rede/grafo), implementado em Python. Carrega dados de pontos de um JSON, constrói um grafo com NetworkX e gera relatórios de conectividade.

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

### Formato do arquivo JSON de entrada

O arquivo JSON deve conter:
- `nodes`: Lista de identificadores de nós
- `edges`: Lista de arestas (pares de nós)

Exemplo (`input.json`):
```json
{
  "nodes": ["1", "2", "3", "4"],
  "edges": [
    ["1", "2"],
    ["1", "3"],
    ["3", "4"],
    ["2", "1"]
  ]
}
```

### Executar análise

```bash
python3 mapeador.py input.json
```

### Saída

O programa gera um relatório em formato JSON com:
- `num_nodes`: Número de nós no grafo
- `num_edges`: Número de arestas na entrada
- `connected_components`: Lista de componentes conectados
- `degrees`: Grau de cada nó
- `is_connected`: Se o grafo é conectado
- `shortest_paths_example`: Exemplos de caminhos mais curtos

Exemplo de saída:
```json
{
    "num_nodes": 4,
    "num_edges": 4,
    "connected_components": [["1", "2", "3", "4"]],
    "degrees": {"1": 2, "2": 1, "3": 2, "4": 1},
    "is_connected": true,
    "shortest_paths_example": {"1": ["1"], "3": ["1", "3"]}
}
```

## Testes

Execute os testes com:
```bash
python3 -m unittest test_mapeador.py -v
```

