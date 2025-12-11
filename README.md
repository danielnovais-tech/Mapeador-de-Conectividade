# Mapeador-de-Conectividade
Repositório para um mapeador simples de conectividade de pontos (nós em uma rede/grafo), implementado em Python. Carrega dados de pontos de um JSON, constrói um grafo com NetworkX e gera relatórios de conectividade.

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

Execute o mapeador:

```bash
python mapeador.py
```

Isso irá:
1. Carregar pontos do arquivo `data/pontos.json`
2. Construir um grafo com NetworkX
3. Gerar um relatório JSON em `data/relatorios/connectivity_report.json`
4. Gerar uma visualização PNG em `data/relatorios/graph_visualization.png`

## Estrutura do Projeto

```
.
├── mapeador.py                          # Script principal
├── requirements.txt                      # Dependências Python
├── data/
│   ├── pontos.json                      # Dados de entrada (pontos e conexões)
│   └── relatorios/
│       ├── connectivity_report.json     # Relatório de conectividade gerado
│       └── graph_visualization.png      # Visualização do grafo
```
