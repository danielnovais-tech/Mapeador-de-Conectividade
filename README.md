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

Execute o programa principal:
```bash
python main.py
```

O programa irá:
1. Carregar os pontos do arquivo `data/pontos.json`
2. Construir um grafo com as conexões entre os pontos
3. Gerar um relatório de conectividade em `data/relatorios/`

## Estrutura de Dados

O arquivo `data/pontos.json` deve seguir o seguinte formato:

```json
{
  "pontos": [
    {
      "id": "A",
      "nome": "Ponto A",
      "conexoes": ["B", "C"]
    },
    {
      "id": "B",
      "nome": "Ponto B",
      "conexoes": ["A"]
    }
  ]
}
```

Cada ponto deve ter:
- `id`: Identificador único do ponto
- `nome`: Nome descritivo do ponto
- `conexoes`: Lista de IDs de outros pontos aos quais este ponto está conectado

## Relatório Gerado

O relatório inclui:
- Número total de nós e arestas
- Número de componentes conectados
- Detalhes de cada nó (nome, grau de conectividade, vizinhos)
- Lista de componentes conectados (se houver mais de um)
