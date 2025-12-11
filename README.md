# Mapeador de Conectividade

Repositório para um mapeador simples de conectividade de pontos (nós em uma rede/grafo), implementado em Python. Carrega dados de pontos de um JSON, constrói um grafo com NetworkX e gera relatórios de conectividade.

## 📋 Características

- **Carregamento de dados**: Lê pontos e suas conexões de arquivos JSON
- **Construção de grafo**: Cria um grafo NetworkX com base nos dados carregados
- **Análise de conectividade**: Calcula estatísticas como densidade, componentes conectados e grau dos nós
- **Relatórios detalhados**: Gera relatórios de texto com todas as informações de conectividade
- **Visualização gráfica**: Cria imagens PNG do grafo para visualização

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/danielnovais-tech/Mapeador-de-Conectividade.git
cd Mapeador-de-Conectividade
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📊 Uso

Execute o programa principal:
```bash
python main.py
```

O programa irá:
1. Carregar os pontos de `data/pontos.json`
2. Construir um grafo NetworkX
3. Gerar um relatório em `data/relatorios/relatorio_YYYYMMDD_HHMMSS.txt`
4. Criar uma visualização em `data/relatorios/grafo_YYYYMMDD_HHMMSS.png`

## 📁 Estrutura do Projeto

```
Mapeador-de-Conectividade/
├── main.py              # Ponto de entrada da aplicação
├── utils.py             # Funções utilitárias
├── requirements.txt     # Dependências Python
├── data/
│   ├── pontos.json     # Arquivo de dados de entrada
│   └── relatorios/     # Diretório de saída (gerado automaticamente)
└── README.md           # Este arquivo
```

## 📝 Formato dos Dados

O arquivo `data/pontos.json` deve seguir este formato:

```json
{
  "pontos": [
    {
      "id": "A",
      "x": 0,
      "y": 0,
      "conecta": ["B", "C"]
    },
    {
      "id": "B",
      "x": 2,
      "y": 1,
      "conecta": ["A", "D"]
    }
  ]
}
```

Cada ponto deve conter:
- `id`: Identificador único do ponto
- `x`, `y`: Coordenadas para visualização
- `conecta`: Lista de IDs de pontos conectados

## 📊 Exemplo de Relatório

```
============================================================
RELATÓRIO DE CONECTIVIDADE
============================================================

Data/Hora: 2025-12-11 20:10:22

ESTATÍSTICAS GERAIS:
  - Número de nós: 7
  - Número de arestas: 6
  - Densidade: 0.2857
  - Componentes conectados: 2

GRAU DOS NÓS:
  - A: 2 conexão(ões)
  - B: 2 conexão(ões)
  ...
```

## 🔧 Dependências

- Python 3.7+
- NetworkX >= 3.0
- Matplotlib >= 3.5.0

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.
