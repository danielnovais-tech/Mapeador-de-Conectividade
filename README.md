# Mapeador de Conectividade

Repositório para um mapeador simples de conectividade de pontos (nós em uma rede/grafo), implementado em Python. Carrega dados de pontos de um JSON, constrói um grafo com NetworkX e gera relatórios de conectividade.

## Descrição

Este projeto implementa um sistema de mapeamento de conectividade que:
- Carrega dados de pontos geográficos de um arquivo JSON
- Constrói um grafo de conectividade usando NetworkX
- Analisa as conexões entre os pontos
- Gera relatórios detalhados sobre a conectividade da rede

## Estrutura do Projeto

```
Mapeador-de-Conectividade/
├── data/
│   └── pontos.json          # Dados dos pontos e suas conexões
├── mapeador.py              # Script principal
├── requirements.txt         # Dependências Python
└── README.md               # Este arquivo
```

## Formato dos Dados

Os pontos são definidos no arquivo `data/pontos.json` com o seguinte formato:

```json
[
  {
    "id": "1",
    "name": "Ponto A (Centro)",
    "lat": -23.5505,
    "lon": -46.6333,
    "neighbors": ["2", "3"]
  }
]
```

Cada ponto contém:
- `id`: Identificador único do ponto
- `name`: Nome descritivo do ponto
- `lat`: Latitude (coordenada geográfica)
- `lon`: Longitude (coordenada geográfica)
- `neighbors`: Lista de IDs dos pontos vizinhos conectados

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

Execute o mapeador de conectividade:

```bash
python3 mapeador.py
```

O script irá:
1. Carregar os dados de `data/pontos.json`
2. Construir o grafo de conectividade
3. Gerar e exibir um relatório completo com:
   - Estatísticas gerais da rede
   - Detalhes de cada ponto (coordenadas, grau, vizinhos)
   - Análise de caminhos entre todos os pontos

## Exemplo de Saída

```
RELATÓRIO DE CONECTIVIDADE
============================================================

Total de pontos: 4
Total de conexões: 3
Grafo conectado: Sim

DETALHES DOS PONTOS:
------------------------------------------------------------

ID: 1
  Nome: Ponto A (Centro)
  Coordenadas: (-23.5505, -46.6333)
  Grau (conexões): 2
  Vizinhos: 2, 3

...

ANÁLISE DE CAMINHOS:
------------------------------------------------------------

Ponto A (Centro) → Ponto D (Leste)
  Caminho: 1 → 3 → 4
  Distância (saltos): 2
```

## Requisitos

- Python 3.7+
- NetworkX 3.0+

## Funcionalidades

- ✅ Carregamento de dados de pontos de arquivo JSON
- ✅ Construção de grafo com NetworkX
- ✅ Análise de conectividade da rede
- ✅ Cálculo de caminhos mais curtos entre pontos
- ✅ Relatórios detalhados de conectividade

## Licença

Este projeto é de código aberto e está disponível sob a licença MIT.
