# Mapeador-de-Conectividade
Repositório para um mapeador simples de conectividade de pontos (nós em uma rede/grafo), implementado em Python. Carrega dados de pontos de um JSON, constrói um grafo com NetworkX e gera relatórios de conectividade.

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

Execute o mapeador de conectividade:

```bash
python src/mapper.py
```

Saída esperada:
```
Carregados 4 pontos.
Grafo construído: 4 nós, 4 arestas.
Relatório gerado em: data/relatorios/connectivity_report.json
```

## Estrutura

- `data/pontos.json` - Dados de entrada com os pontos a serem mapeados
- `src/mapper.py` - Script principal do mapeador
- `data/relatorios/connectivity_report.json` - Relatório de conectividade gerado

## Funcionalidades

- Carrega pontos de um arquivo JSON
- Constrói um grafo com NetworkX conectando os pontos
- Gera um relatório detalhado de conectividade em formato JSON
