# Mapeador-de-Conectividade

Repositório para um mapeador simples de conectividade de pontos (nós em uma rede/grafo), implementado em Python. Carrega dados de pontos de um JSON, constrói um grafo com NetworkX e gera relatórios de conectividade.

## Funcionalidades

- 📍 **Carregamento de Pontos**: Lê dados de pontos de um arquivo JSON com tratamento robusto de erros
- 🕸️ **Construção de Grafo**: Cria um grafo NetworkX baseado nas conexões entre pontos
- 📦 **Sistema de Cache**: Cache inteligente para construção de grafos, evitando reconstruções desnecessárias
- 📊 **Relatório de Conectividade**: Gera relatórios detalhados em JSON incluindo:
  - Número de nós e arestas
  - Componentes conectados
  - Graus de cada nó
  - Status de conectividade
  - Exemplo de caminho mais curto
- 📈 **Visualização**: Cria visualizações gráficas posicionadas por coordenadas geográficas (lat/lon)
- 📝 **Sistema de Logging**: Registra todas as operações com métricas de performance
- 🤖 **Integração com IA (Opcional)**: Análise de grafos usando DeepSeek AI

## Estrutura do Projeto

```
Mapeador-de-Conectividade/
├── models.py              # Modelo de dados Point
├── connectivity_mapper.py # Funções principais do mapeador
├── cache_manager.py       # Sistema de cache para grafos
├── ai_integration.py      # Integração opcional com DeepSeek
├── example.py             # Exemplo de uso
├── data/                  # Dados de entrada
│   └── points.json        # Pontos de exemplo
├── logs/                  # Arquivos de log
├── requirements.txt       # Dependências do projeto
└── README.md             # Este arquivo
```

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

**Nota**: A dependência `openai` é opcional e necessária apenas para análise com IA usando DeepSeek.

## Uso

### Exemplo Básico

Execute o script de exemplo:
```bash
python example.py
```

Este script irá:
1. Carregar pontos do arquivo `data/points.json`
2. Construir um grafo de conectividade com cache
3. Gerar um relatório em `output/connectivity_report.json`
4. Criar uma visualização em `output/graph_visualization.png`
5. (Opcional) Gerar análise de IA se configurado

### Uso Programático

```python
from connectivity_mapper import load_points, build_graph, generate_report, visualize_graph
from cache_manager import CachedGraphBuilder

# Carregar pontos com tratamento de erros
try:
    points = load_points('data/points.json')
except FileNotFoundError as e:
    print(f"Arquivo não encontrado: {e}")
except json.JSONDecodeError as e:
    print(f"Erro ao decodificar JSON: {e}")

# Construir grafo com cache
cache_builder = CachedGraphBuilder()
G = cache_builder.build_graph(points)

# Gerar relatório
report_file = generate_report(G, 'output')

# Visualizar grafo
viz_file = visualize_graph(G, 'output')
```

## Tratamento de Erros

O sistema implementa tratamento robusto de erros em todas as funções principais:

- **`load_points()`**: Trata `FileNotFoundError`, `json.JSONDecodeError` e erros de validação
- **`build_graph()`**: Valida dados de entrada e trata casos de grafos vazios
- **`generate_report()`**: Trata erros de I/O e permissões
- **`visualize_graph()`**: Trata erros de matplotlib e coordenadas inválidas

Todas as exceções são registradas no sistema de logging e exibidas ao usuário.

## Sistema de Cache

O sistema de cache evita reconstruir grafos idênticos:

```python
from cache_manager import CachedGraphBuilder

cache_builder = CachedGraphBuilder()

# Primeira chamada - constrói e armazena no cache
G1 = cache_builder.build_graph(points)  # ✨ Grafo construído e armazenado no cache

# Segunda chamada com os mesmos dados - recupera do cache
G2 = cache_builder.build_graph(points)  # 📦 Grafo recuperado do cache

# Limpar cache se necessário
cache_builder.clear_cache()  # 🧹 Cache limpo
```

O cache usa hash MD5 dos dados dos pontos para identificar grafos únicos.

## Sistema de Logging

O sistema registra todas as operações em arquivos de log com rotação diária:

- **Local dos logs**: `logs/mapper_YYYYMMDD.log`
- **Formato**: `timestamp - level - message`
- **Informações registradas**:
  - Operações de carregamento de pontos
  - Construção de grafos
  - Geração de relatórios
  - Visualizações
  - Métricas de tempo de execução
  - Erros e avisos

Exemplo de log:
```
2024-01-15 10:30:45 - INFO - Carregando pontos de data/points.json
2024-01-15 10:30:45 - INFO - ✅ 4 pontos carregados com sucesso
2024-01-15 10:30:45 - INFO - Construindo grafo com 4 pontos
2024-01-15 10:30:45 - INFO - ✅ Grafo construído: 4 nós, 5 arestas
2024-01-15 10:30:46 - INFO - ✅ Relatório gerado com sucesso em 0.05s: output/connectivity_report.json
```

## Integração com DeepSeek (Opcional)

Para análise de grafos com IA, você pode usar a integração opcional com DeepSeek:

### Instalação
```bash
pip install openai
```

### Configuração

Configure sua API key do DeepSeek:
```bash
export DEEPSEEK_API_KEY="sua-api-key-aqui"
```

Ou passe diretamente no código:
```python
from ai_integration import generate_ai_report

# Gera relatório com análise de IA
ai_report = generate_ai_report(G, 'output', api_key='sua-api-key')
```

### Recursos da Análise de IA

A análise com IA fornece insights sobre:
1. **Topologia da rede**: Estrutura e características do grafo
2. **Pontos críticos de falha**: Nós que podem comprometer a conectividade
3. **Sugestões de otimização**: Melhorias recomendadas para a rede
4. **Métricas de robustez**: Avaliação da resistência da rede

### Uso Programático

```python
from ai_integration import DeepSeekAnalyzer, DEEPSEEK_AVAILABLE

if DEEPSEEK_AVAILABLE:
    analyzer = DeepSeekAnalyzer(api_key='sua-api-key')
    analysis = analyzer.analyze_graph(G)
    print(analysis)
else:
    print("DeepSeek não disponível. Instale: pip install openai")
```

## Formato de Dados

O arquivo JSON de entrada deve seguir o formato:

```json
[
    {
        "id": "1",
        "name": "Ponto A",
        "lat": -23.5505,
        "lon": -46.6333,
        "neighbors": ["2", "3"]
    },
    ...
]
```

### Campos:
- `id`: Identificador único do ponto
- `name`: Nome descritivo do ponto
- `lat`: Latitude (coordenada geográfica)
- `lon`: Longitude (coordenada geográfica)
- `neighbors`: Lista de IDs dos pontos vizinhos conectados

## Exemplos Avançados

### Construir múltiplos grafos com cache

```python
from cache_manager import CachedGraphBuilder
from connectivity_mapper import load_points

cache_builder = CachedGraphBuilder()

# Carregar e processar diferentes conjuntos de dados
points1 = load_points('data/network1.json')
points2 = load_points('data/network2.json')

G1 = cache_builder.build_graph(points1)  # Constrói e armazena
G2 = cache_builder.build_graph(points2)  # Constrói e armazena
G1_cached = cache_builder.build_graph(points1)  # Recupera do cache
```

### Tratamento completo de erros

```python
from connectivity_mapper import load_points, build_graph, generate_report, visualize_graph
import logging

try:
    # Carregar pontos
    points = load_points('data/points.json')
    
    # Construir grafo
    G = build_graph(points)
    
    # Gerar relatório
    report_file = generate_report(G, 'output')
    
    # Visualizar grafo
    viz_file = visualize_graph(G, 'output')
    
    print("✅ Processo concluído com sucesso!")
    
except FileNotFoundError as e:
    logging.error(f"Arquivo não encontrado: {e}")
except ValueError as e:
    logging.error(f"Dados inválidos: {e}")
except Exception as e:
    logging.error(f"Erro inesperado: {e}")
```

## Dependências

- `networkx>=3.0` - Para operações de grafos
- `matplotlib>=3.5.0` - Para visualização
- `openai>=1.0.0` - (Opcional) Para integração com DeepSeek AI

## Licença

Este projeto é de código aberto e está disponível sob a licença MIT.
