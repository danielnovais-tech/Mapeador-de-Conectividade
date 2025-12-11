# Mapeador-de-Conectividade
Repositório para um mapeador simples de conectividade de pontos (nós em uma rede/grafo), implementado em Python. Carrega dados de pontos de um JSON, constrói um grafo com NetworkX e gera relatórios de conectividade.

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

Execute o script principal para gerar o relatório de conectividade:

```bash
python mapeador.py
```

O script irá:
1. Carregar os dados dos pontos do arquivo `data/pontos.json`
2. Construir um grafo com NetworkX
3. Gerar um relatório completo de conectividade incluindo:
   - Número de pontos e conexões
   - Verificação se o grafo é conexo
   - Detalhes de cada ponto (coordenadas, vizinhos)
   - Caminhos mais curtos entre todos os pares de pontos
   - Estatísticas do grafo (densidade, grau médio, diâmetro)

## Estrutura dos Dados

Os dados dos pontos são armazenados em `data/pontos.json` no seguinte formato:

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
- `lat`: Latitude
- `lon`: Longitude
- `neighbors`: Lista de IDs dos pontos vizinhos (conectados)
