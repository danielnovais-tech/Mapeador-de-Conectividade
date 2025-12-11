# Mapeador-de-Conectividade
Repositório para um mapeador simples de conectividade de pontos (nós em uma rede/grafo), implementado em Python. Carrega dados de pontos de um JSON, constrói um grafo com NetworkX e gera relatórios de conectividade.

## Instalação

```bash
pip install -e .
```

## Estrutura do Projeto

- `src/mapeador_conectividade/`: Código fonte principal
  - `models.py`: Define o dataclass `Point` para representar pontos no grafo
- `tests/`: Testes unitários
- `example.py`: Script de exemplo demonstrando uso da biblioteca

## Uso

### Point Dataclass

O `Point` é um dataclass que representa um nó na rede com as seguintes propriedades:

- `id` (str): Identificador único do ponto
- `name` (str): Nome descritivo do ponto
- `lat` (float): Latitude (coordenada geográfica)
- `lon` (float): Longitude (coordenada geográfica)
- `neighbors` (List[str]): Lista de IDs dos pontos vizinhos conectados

```python
from mapeador_conectividade import Point

# Criar um ponto
point = Point(
    id="p1",
    name="São Paulo",
    lat=-23.5505,
    lon=-46.6333,
    neighbors=["p2", "p3"]
)
```

## Testes

```bash
python tests/test_models.py
```

## Exemplo

```bash
python example.py
```
