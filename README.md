# Mapeador de Conectividade Rural

Sistema para mapear e analisar pontos de conectividade em áreas rurais, fornecendo dados detalhados sobre qualidade de conexão, localização geográfica e infraestrutura de internet.

## Características

- 📍 Geolocalização de pontos de conectividade
- 🚀 Testes de velocidade de internet (download/upload/latência)
- 📊 Relatórios em múltiplos formatos (TXT/JSON/CSV)
- 🗺️ Mapeamento de comunidades rurais
- 📈 Análise de qualidade de conexão
- 🔍 Importação e exportação de dados

## Instalação

```bash
# Clone o repositório
git clone https://github.com/danielnovais-tech/Mapeador-de-Conectividade.git
cd Mapeador-de-Conectividade

# Instale as dependências
pip install -r requirements.txt
```

## Dependências

O projeto utiliza as seguintes bibliotecas Python:

- `requests` - Requisições HTTP
- `speedtest-cli` - Testes de velocidade de internet
- `geopy` - Geocodificação e serviços de localização
- `pandas` - Manipulação e análise de dados
- `tabulate` - Formatação de tabelas
- `pytest` - Framework de testes

## Uso

### Argumentos de Linha de Comando (CLI)

```bash
python main.py [OPÇÕES]
```

#### Opções Disponíveis:

- `--debug` - Ativa o modo debug com logs detalhados
- `--relatorio` - Gera relatórios de conectividade em múltiplos formatos
- `--importar` - Importa dados de conectividade de arquivos externos

### Exemplos de Uso

```bash
# Modo normal
python main.py

# Com modo debug ativo
python main.py --debug

# Gerar relatório de conectividade
python main.py --relatorio

# Importar dados de arquivo
python main.py --importar dados_conectividade.json

# Combinar múltiplas opções
python main.py --debug --relatorio
```

## Fluxo de Trabalho Típico

1. **Coleta de Dados**
   - Execute o mapeador para coletar dados de conectividade
   - O sistema registra automaticamente geolocalização e métricas de velocidade

2. **Análise**
   - Use `--relatorio` para gerar análises detalhadas
   - Revise os dados em formato TXT, JSON ou CSV

3. **Importação/Exportação**
   - Importe dados históricos com `--importar`
   - Exporte resultados para análise externa

4. **Depuração**
   - Use `--debug` para troubleshooting e logs detalhados

## Estrutura de Dados

### Ponto de Conectividade

Cada ponto de conectividade armazenado contém as seguintes informações:

```python
{
    "id": int,                          # Identificador único
    "comunidade": str,                  # Nome da comunidade rural
    "latitude": float,                  # Coordenada de latitude
    "longitude": float,                 # Coordenada de longitude
    "provedor": str,                    # Provedor de internet
    "tipo_conexao": str,                # Tipo (Fibra, Rádio, Satélite, etc.)
    "velocidade_download": float,       # Velocidade em Mbps
    "velocidade_upload": float,         # Velocidade em Mbps
    "latencia": float,                  # Latência em ms
    "data_coleta": str,                 # Data/hora da coleta (ISO 8601)
    "conexoes": int                     # Número de conexões ativas
}
```

### Exemplo de Dados

```json
{
    "id": 1,
    "comunidade": "Vila Rural São José",
    "latitude": -15.7942,
    "longitude": -47.8822,
    "provedor": "InternetRural",
    "tipo_conexao": "Rádio",
    "velocidade_download": 10.5,
    "velocidade_upload": 2.3,
    "latencia": 45.2,
    "data_coleta": "2025-12-11T23:15:00Z",
    "conexoes": 25
}
```

## Recursos Técnicos

### 1. Testes de Velocidade

Utiliza `speedtest-cli` para medir:
- Velocidade de download
- Velocidade de upload
- Latência (ping)

```python
# Exemplo de teste de velocidade
import speedtest
st = speedtest.Speedtest()
download_speed = st.download() / 1_000_000  # Mbps
upload_speed = st.upload() / 1_000_000      # Mbps
latency = st.results.ping                   # ms
```

### 2. Geocodificação

Usa `geopy` para converter endereços em coordenadas:

```python
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="mapeador_conectividade")
location = geolocator.geocode("Comunidade Rural")
```

### 3. Formatos de Relatório

- **TXT**: Relatório legível por humanos
- **JSON**: Formato estruturado para APIs
- **CSV**: Compatível com Excel e análise de dados

## Estrutura do Projeto

```
Mapeador-de-Conectividade/
├── main.py              # Script principal
├── models.py            # Modelos de dados
├── requirements.txt     # Dependências
├── tests/              # Testes unitários
│   ├── __init__.py
│   ├── test_connectivity.py
│   └── test_reports.py
├── data/               # Dados coletados
│   ├── connectivity_data.json
│   └── reports/
└── README.md           # Documentação
```

## Testes

O projeto utiliza `pytest` para testes automatizados.

### Executar Todos os Testes

```bash
pytest
```

### Executar Testes Específicos

```bash
# Testes de conectividade
pytest tests/test_connectivity.py

# Testes de relatórios
pytest tests/test_reports.py

# Com saída detalhada
pytest -v

# Com cobertura de código
pytest --cov=. --cov-report=html
```

### Estrutura de Testes

```python
# Exemplo de teste
def test_speed_measurement():
    """Testa a medição de velocidade"""
    result = measure_speed()
    assert result['download'] > 0
    assert result['upload'] > 0
    assert result['latency'] > 0
```

## Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

Daniel Novais - [@danielnovais-tech](https://github.com/danielnovais-tech)

Link do Projeto: [https://github.com/danielnovais-tech/Mapeador-de-Conectividade](https://github.com/danielnovais-tech/Mapeador-de-Conectividade)

---

**Nota**: Este sistema foi desenvolvido para auxiliar no mapeamento de conectividade em áreas rurais, contribuindo para a inclusão digital e melhor planejamento de infraestrutura de internet.
