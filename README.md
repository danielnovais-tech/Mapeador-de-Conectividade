# Mapeador de Conectividade Rural

Um aplicativo Python para mapear pontos de acesso à internet em comunidades rurais, com foco em conexões Starlink e outras tecnologias.

## 🎯 Objetivo

Auxiliar governos, ONGs e comunidades a:
- Mapear pontos de acesso à internet existentes
- Medir qualidade de conexão (velocidade, latência)
- Gerar relatórios para expansão de infraestrutura
- Identificar áreas com baixa conectividade

## ✨ Funcionalidades

- ✅ Cadastro de pontos de acesso com geolocalização
- ✅ Medição automática de velocidade da internet
- ✅ Teste de conectividade com sites essenciais
- ✅ Geração de relatórios em múltiplos formatos (TXT, JSON, HTML, CSV)
- ✅ **Relatórios personalizados interativos** com filtros e opções customizáveis
- ✅ Identificação automática de pontos críticos (< 10 Mbps)
- ✅ Recomendações automáticas de upgrade e expansão
- ✅ Busca e filtragem por comunidade/provedor
- ✅ Estatísticas detalhadas com médias, mínimos e máximos
- ✅ Interface CLI colorida e amigável
- ✅ Persistência de dados em JSON
- ✅ Visualização de conectividade em grafos

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

### Interface CLI para Relatórios

Use a interface de linha de comando para gerar relatórios interativamente:

```bash
python gerar_relatorio_cli.py
```

A CLI oferece:
- Menu interativo com 6 opções de relatório
- Geração de relatórios em múltiplos formatos (TXT, JSON, HTML, CSV)
- **Relatório Personalizado Interativo** com opções selecionáveis:
  - ✅ Estatísticas gerais
  - ✅ Lista completa de pontos
  - ⚙️ Apenas pontos com medição
  - ⚙️ Apenas pontos críticos (< 10 Mbps)
  - ⚙️ Recomendações automáticas
  - ⚙️ Metodologia de coleta

### Uso Programático

Você também pode usar a classe `MapeadorConectividade` diretamente em seu código:

```python
from main import MapeadorConectividade
from relatorios import GeradorRelatorios

# Criar instância
mapeador = MapeadorConectividade(data_dir='data')

# Executar análise completa
mapeador.executar()

# Ou executar etapas individuais
mapeador.load_points()
mapeador.build_graph()
relatorio = mapeador.generate_report()
visualizacao = mapeador.visualize_graph()

# Gerar relatórios em múltiplos formatos
gerador = GeradorRelatorios(output_dir='data/relatorios')
pontos = mapeador.load_points()

# Gerar relatórios individuais
txt_file = gerador.gerar_relatorio_txt(pontos)
json_file = gerador.gerar_relatorio_json(pontos)
html_file = gerador.gerar_relatorio_html(pontos)
csv_file = gerador.gerar_relatorio_csv(pontos)

# Ou gerar todos os formatos de uma vez
relatorios = gerador.gerar_relatorio_completo(pontos, formatos=['txt', 'json', 'html', 'csv'])

# Gerar relatório personalizado programaticamente
relatorio_custom = gerador.gerar_relatorio_personalizado(
    pontos,
    estatisticas=stats,
    opcoes=['1', '4', '5']  # Estatísticas, críticos e recomendações
)

# Ou modo interativo (sem passar opcoes)
relatorio_interativo = gerador.gerar_relatorio_personalizado(pontos, stats)
```

## 📁 Estrutura do Projeto

```
mapeador-conectividade/
├── main.py                      # Interface principal com tratamento de erros
├── models.py                    # Classes de dados
├── relatorios.py                # Gerador de relatórios em múltiplos formatos
├── gerar_relatorio_cli.py       # Interface CLI para geração de relatórios
├── utils.py                     # Funções utilitárias completas
├── data/
│   ├── pontos.json             # Dados de exemplo
│   └── relatorios/             # Relatórios gerados
├── requirements.txt             # Dependências
├── .gitignore                   # Arquivos ignorados no Git
└── README.md                    # Documentação completa
```

## 📝 Formato dos Dados

O arquivo `data/pontos.json` suporta dois formatos:

### Formato Simples (Grafo de Conectividade)
```json
{
  "pontos": [
    {
      "id": "A",
      "x": 0,
      "y": 0,
      "conecta": ["B", "C"]
    }
  ]
}
```

### Formato Completo (Pontos de Acesso Rural)
```json
{
  "pontos": [
    {
      "id": "PA001",
      "nome": "Centro Comunitário Vila Nova",
      "latitude": -15.7942,
      "longitude": -47.8822,
      "comunidade": "Vila Nova",
      "provedor": "Starlink",
      "tecnologia": "Satélite",
      "velocidade_download": 150.5,
      "velocidade_upload": 20.3,
      "latencia": 45,
      "status": "ativo",
      "observacoes": "Ponto principal da comunidade"
    }
  ]
}
```

## 📊 Relatórios

O sistema gera relatórios detalhados em múltiplos formatos através da classe `GeradorRelatorios`:

### Formatos Suportados

1. **TXT**: Relatório de texto formatado com cabeçalho, estatísticas e lista detalhada de pontos
2. **JSON**: Dados estruturados em formato JSON para integração com outros sistemas
3. **HTML**: Relatório web interativo com tabelas estilizadas e estatísticas visuais
4. **CSV**: Planilha para análise em Excel ou ferramentas de dados

### Conteúdo dos Relatórios

- Estatísticas de velocidade (download/upload/latência)
  - Médias, mínimos e máximos
  - Total de medições
- Análise de latência
- Distribuição por comunidade e provedor
- Análise de conectividade entre pontos
- Grafos visuais de conectividade
- Componentes conectados e isolados
- Lista detalhada de todos os pontos com:
  - Identificação e localização
  - Velocidades medidas
  - Status operacional
  - Observações

### Exemplo de Uso

```python
from relatorios import GeradorRelatorios
from utils import calcular_estatisticas_velocidade

gerador = GeradorRelatorios(output_dir='data/relatorios')

# Carregar pontos
pontos = [...]  # Lista de pontos

# Calcular estatísticas
stats = calcular_estatisticas_velocidade(pontos)

# Gerar todos os formatos
relatorios = gerador.gerar_relatorio_completo(
    pontos, 
    estatisticas=stats,
    formatos=['txt', 'json', 'html', 'csv']
)
```

## 🔧 Dependências

### Principais
- Python 3.7+
- NetworkX >= 3.0 - Análise de grafos
- Matplotlib >= 3.5.0 - Visualizações
- Pandas >= 2.1.4 - Manipulação de dados
- Requests >= 2.31.0 - Testes de conectividade
- Speedtest-cli >= 2.1.3 - Medição de velocidade
- Geopy >= 2.4.1 - Cálculos geográficos
- Tabulate >= 0.9.0 - Formatação de tabelas
- Colorama >= 0.4.6 - Cores no terminal

### Desenvolvimento
- pytest >= 7.4.3 - Testes
- black >= 23.11.0 - Formatação de código
- flake8 >= 6.1.0 - Linting

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:
1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 🌟 Casos de Uso

- **Governos**: Planejamento de expansão de infraestrutura digital
- **ONGs**: Monitoramento de projetos de inclusão digital
- **Comunidades**: Mapeamento colaborativo de pontos de acesso
- **Pesquisadores**: Análise de conectividade em áreas rurais
- **Provedores**: Identificação de oportunidades de expansão

