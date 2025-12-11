# Mapeador de Conectividade

Um mapeador simples e prático de conectividade de pontos (nós em uma rede/grafo), implementado em Python.

## 📋 Descrição

Este projeto analisa conectividade entre pontos de uma rede. Carrega dados de pontos de um arquivo JSON, constrói um grafo com NetworkX e gera relatórios detalhados de conectividade.

## ✨ Funcionalidades

- ✅ Carregamento de pontos a partir de arquivo JSON
- ✅ Construção automática de grafo com NetworkX
- ✅ Validação de conexões (ignora nós inexistentes)
- ✅ Detecção de componentes conectados
- ✅ Análise de grau de conectividade de cada nó
- ✅ Geração de relatórios com timestamp
- ✅ Tratamento robusto de erros

## 📦 Instalação

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passos de instalação

1. Clone o repositório:
```bash
git clone https://github.com/danielnovais-tech/Mapeador-de-Conectividade.git
cd Mapeador-de-Conectividade
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🚀 Uso

### Execução básica

```bash
python main.py
```

### O que o programa faz:

1. Carrega os pontos do arquivo `data/pontos.json`
2. Constrói um grafo com as conexões entre os pontos
3. Gera um relatório de conectividade em `data/relatorios/`

### Exemplo de saída:

```
Carregados 6 pontos.
Grafo construído: 6 nós, 5 arestas.
Relatório gerado em: data/relatorios/relatorio_20251211_153045.txt
```

## 📊 Estrutura de Dados

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
      "conexoes": ["A", "D"]
    },
    {
      "id": "C",
      "nome": "Ponto C",
      "conexoes": ["A"]
    }
  ]
}
```

### Campos obrigatórios:

- **`id`** (string): Identificador único do ponto
- **`nome`** (string): Nome descritivo do ponto
- **`conexoes`** (array): Lista de IDs de outros pontos aos quais este ponto está conectado

## 📝 Relatório Gerado

O relatório inclui as seguintes informações:

### Informações Gerais
- Número total de nós (pontos)
- Número total de arestas (conexões)
- Número de componentes conectados

### Detalhes por Nó
Para cada ponto, o relatório mostra:
- ID e nome do nó
- Grau de conectividade (número de conexões)
- Lista de vizinhos (pontos conectados)

### Componentes Conectados
Se houver mais de um componente conectado (subgrafos isolados), o relatório lista cada componente separadamente.

### Exemplo de relatório:

```
============================================================
RELATÓRIO DE CONECTIVIDADE
============================================================

Total de nós: 6
Total de arestas: 5

Número de componentes conectados: 2

------------------------------------------------------------
DETALHES DOS NÓS
------------------------------------------------------------

Nó: A
  Nome: Ponto A
  Grau de conectividade: 2
  Conectado a: ['B', 'C']

Nó: F
  Nome: Ponto F (isolado)
  Grau de conectividade: 0
  Conectado a: []

------------------------------------------------------------
COMPONENTES CONECTADOS
------------------------------------------------------------

Componente 1: ['A', 'B', 'C', 'D', 'E']
Componente 2: ['F']

============================================================
Relatório gerado em: 2025-12-11 15:30:45
============================================================
```

## 🗂️ Estrutura do Projeto

```
Mapeador-de-Conectividade/
├── main.py                      # Ponto de entrada principal
├── utils.py                     # Funções utilitárias
├── requirements.txt             # Dependências do projeto
├── .gitignore                   # Arquivos ignorados pelo Git
├── README.md                    # Este arquivo
└── data/
    ├── pontos.json             # Dados de entrada (exemplo incluído)
    └── relatorios/             # Relatórios gerados (criado automaticamente)
        └── .gitkeep
```

## 🛠️ Dependências

- **networkx** >= 3.0: Biblioteca para criação e análise de grafos

## 🔧 Tratamento de Erros

O programa inclui validações robustas:

- ✅ Verifica se o arquivo `pontos.json` existe
- ✅ Valida a estrutura do JSON (presença da chave `pontos`)
- ✅ Ignora conexões para nós inexistentes (com aviso)
- ✅ Captura e reporta erros de forma amigável

## 🚀 Roadmap

Possíveis melhorias futuras:

- [ ] Visualização gráfica do grafo (matplotlib/graphviz)
- [ ] Exportação de relatórios em múltiplos formatos (CSV, JSON, PDF)
- [ ] Interface web com Flask/Django
- [ ] Métricas avançadas de rede (centralidade, clustering)
- [ ] Suporte a grafos direcionados e ponderados
- [ ] Testes unitários com pytest

## 📄 Licença

Este projeto está disponível como código aberto para fins educacionais e de análise de conectividade.

## 👤 Autor

**Daniel Novais** ([@danielnovais-tech](https://github.com/danielnovais-tech))

---

*Última atualização: 11 de dezembro de 2025*