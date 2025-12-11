# Mapeador-de-Conectividade

Repositório para um mapeador simples de conectividade de pontos (nós em uma rede/grafo), implementado em Python. Carrega dados de pontos de um JSON, constrói um grafo com NetworkX e gera relatórios de conectividade.

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/danielnovais-tech/Mapeador-de-Conectividade.git
cd Mapeador-de-Conectividade
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

Execute o script principal para analisar o grafo definido em `graph_data.json`:

```bash
python connectivity_mapper.py
```

### Formato de Entrada

O arquivo `graph_data.json` deve conter:
- `nodes`: Lista de IDs dos nós (strings)
- `edges`: Lista de arestas, onde cada aresta é um par de IDs de nós

Exemplo:
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

### Formato de Saída

O programa gera um relatório JSON com as seguintes métricas:
- `num_nodes`: Número total de nós no grafo
- `num_edges`: Número total de arestas no grafo
- `connected_components`: Lista de componentes conectados
- `degrees`: Grau de cada nó (número de conexões)
- `is_connected`: Booleano indicando se o grafo é totalmente conectado
- `shortest_paths_example`: Exemplos de caminhos mais curtos a partir do primeiro nó

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

## Funcionalidades

- **Análise de Conectividade**: Identifica componentes conectados no grafo
- **Cálculo de Graus**: Calcula o grau de cada nó
- **Caminhos Mais Curtos**: Calcula caminhos mais curtos entre nós usando NetworkX
- **Verificação de Conectividade**: Verifica se todos os nós estão conectados

## Requisitos

- Python 3.6+
- NetworkX 3.0+

