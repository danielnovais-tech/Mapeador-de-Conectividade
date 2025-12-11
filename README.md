# Mapeador-de-Conectividade

Repositório para um mapeador simples de conectividade de pontos (nós em uma rede/grafo), implementado em Python. Carrega dados de pontos de um JSON, constrói um grafo com NetworkX e gera relatórios de conectividade.

## Estrutura do Projeto

```
.
├── models.py                 # Classe Point para representar pontos
├── connectivity_mapper.py    # Funções principais (load_points, build_graph, generate_report)
├── main.py                   # Script de demonstração
├── requirements.txt          # Dependências do projeto
├── data/
│   └── points.json          # Dados de exemplo
└── output/
    └── connectivity_report.json  # Relatório gerado
```

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

### Executar o script de demonstração:

```bash
python main.py
```

### Usar como módulo:

```python
from connectivity_mapper import load_points, build_graph, generate_report

# Carregar pontos do arquivo JSON
points = load_points('data/points.json')

# Construir grafo
G = build_graph(points)

# Gerar relatório
report_file = generate_report(G, 'output')
```

## Formato dos Dados

Os pontos devem ser fornecidos em um arquivo JSON com a seguinte estrutura:

```json
[
    {
        "id": "1",
        "name": "Ponto A",
        "lat": -23.5505,
        "lon": -46.6333,
        "neighbors": ["2", "3"]
    }
]
```

## Funcionalidades

- **load_points**: Carrega pontos de um arquivo JSON
- **build_graph**: Constrói um grafo NetworkX a partir dos pontos
- **generate_report**: Gera relatório de conectividade com:
  - Número de nós e arestas
  - Componentes conectados
  - Grau de cada nó
  - Status de conectividade
  - Exemplo de caminho mais curto

