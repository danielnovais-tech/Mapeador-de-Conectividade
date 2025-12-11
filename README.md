# Mapeador-de-Conectividade

Repositório para um mapeador simples de conectividade de pontos (nós em uma rede/grafo), implementado em Python. Carrega dados de pontos de um JSON, constrói um grafo com NetworkX e gera relatórios de conectividade.

## Funcionalidades

- 📍 **Carregamento de Pontos**: Lê dados de pontos de um arquivo JSON
- 🕸️ **Construção de Grafo**: Cria um grafo NetworkX baseado nas conexões entre pontos
- 📊 **Relatório de Conectividade**: Gera relatórios detalhados em JSON incluindo:
  - Número de nós e arestas
  - Componentes conectados
  - Graus de cada nó
  - Status de conectividade
  - Exemplo de caminho mais curto
- 📈 **Visualização**: Cria visualizações gráficas posicionadas por coordenadas geográficas (lat/lon)

## Estrutura do Projeto

```
Mapeador-de-Conectividade/
├── models.py              # Modelo de dados Point
├── connectivity_mapper.py # Funções principais do mapeador
├── example.py             # Exemplo de uso
├── data/                  # Dados de entrada
│   └── points.json        # Pontos de exemplo
├── requirements.txt       # Dependências do projeto
└── README.md             # Este arquivo
```

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

### Exemplo Básico

Execute o script de exemplo:
```bash
python example.py
```

Este script irá:
1. Carregar pontos do arquivo `data/points.json`
2. Construir um grafo de conectividade
3. Gerar um relatório em `output/connectivity_report.json`
4. Criar uma visualização em `output/graph_visualization.png`

### Uso Programático

```python
from connectivity_mapper import load_points, build_graph, generate_report, visualize_graph

# Carregar pontos
points = load_points('data/points.json')

# Construir grafo
G = build_graph(points)

# Gerar relatório
report_file = generate_report(G, 'output')

# Visualizar grafo
viz_file = visualize_graph(G, 'output')
```

## Formato de Dados

O arquivo JSON de entrada deve seguir o formato:

```json
[
    {
        "id": "1",
        "name": "Ponto A",
        "lat": -23.5505,
        "lon": -46.6333,
        "neighbors": ["2", "3"]
    },
    ...
]
```

### Campos:
- `id`: Identificador único do ponto
- `name`: Nome descritivo do ponto
- `lat`: Latitude (coordenada geográfica)
- `lon`: Longitude (coordenada geográfica)
- `neighbors`: Lista de IDs dos pontos vizinhos conectados

## Dependências

- `networkx>=3.0` - Para operações de grafos
- `matplotlib>=3.5.0` - Para visualização

## Licença

Este projeto é de código aberto e está disponível sob a licença MIT.
