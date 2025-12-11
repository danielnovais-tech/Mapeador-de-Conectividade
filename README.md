# Mapeador-de-Conectividade

Repositório para um mapeador simples de conectividade de pontos (nós em uma rede/grafo), implementado em Python. Carrega dados de pontos de um JSON, constrói um grafo com NetworkX e gera relatórios de conectividade.

## Instalação

```bash
pip install -e .
```

## Estrutura do Projeto

- `mapeador_conectividade/`: Pacote principal
  - `point.py`: Define a classe `Point` para representar nós na rede
- `tests/`: Testes unitários
- `example.py`: Exemplo de uso

## Uso

### Classe Point

A classe `Point` representa um ponto/nó em uma rede de conectividade:

```python
from mapeador_conectividade import Point

# Criar um ponto
point = Point(
    id="p1",
    name="Ponto 1",
    lat=-23.5505,
    lon=-46.6333,
    neighbors=["p2", "p3"]  # IDs dos vizinhos conectados
)
```

### Exemplo

Execute o exemplo incluído:

```bash
python example.py
```

## Testes

Execute os testes:

```bash
python -m unittest discover tests
```

## Estrutura da Classe Point

- `id` (str): Identificador único do ponto
- `name` (str): Nome legível do ponto
- `lat` (float): Coordenada de latitude
- `lon` (float): Coordenada de longitude
- `neighbors` (List[str]): Lista de IDs dos pontos vizinhos conectados
