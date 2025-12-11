# Mapeador-de-Conectividade

Repositório para um mapeador simples de conectividade de pontos (nós em uma rede/grafo), implementado em Python. Carrega dados de pontos de um JSON, constrói um grafo com NetworkX e gera relatórios de conectividade.

## Requisitos

- Python 3.6+
- NetworkX 2.5+

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

1. Configure o grafo de entrada no arquivo `input_graph.json` com o formato:
```json
{
  "nodes": ["1", "2", "3", "4"],
  "edges": [
    ["1", "2"],
    ["1", "3"],
    ["3", "4"],
    ["1", "3"]
  ]
}
```

2. Execute o mapeador de conectividade:
```bash
python3 connectivity_mapper.py
```

3. O resultado será exibido no console e salvo em `output_analysis.json`

## Formato de Saída

O sistema gera uma análise de conectividade com as seguintes informações:

- `num_nodes`: Número de nós no grafo
- `num_edges`: Número de arestas no grafo
- `connected_components`: Componentes conexos do grafo
- `degrees`: Grau de cada nó
- `is_connected`: Se o grafo é conexo
- `shortest_paths_example`: Exemplos de caminhos mais curtos a partir do nó "1"

## Exemplo de Saída

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

