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
- ✅ Geração de relatórios em múltiplos formatos
- ✅ Busca e filtragem por comunidade/provedor
- ✅ Estatísticas detalhadas
- ✅ Interface de linha de comando amigável
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

### Uso Programático

Você também pode usar a classe `MapeadorConectividade` diretamente em seu código:

```python
from main import MapeadorConectividade

# Criar instância
mapeador = MapeadorConectividade(data_dir='data')

# Executar análise completa
mapeador.executar()

# Ou executar etapas individuais
mapeador.load_points()
mapeador.build_graph()
relatorio = mapeador.generate_report()
visualizacao = mapeador.visualize_graph()
```

## 📁 Estrutura do Projeto

```
mapeador-conectividade/
├── main.py                      # Interface principal com tratamento de erros
├── models.py                    # Classes de dados
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

O sistema gera relatórios detalhados incluindo:
- Estatísticas de velocidade (download/upload)
- Análise de latência
- Distribuição por comunidade e provedor
- Análise de conectividade entre pontos
- Grafos visuais de conectividade
- Componentes conectados e isolados

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

