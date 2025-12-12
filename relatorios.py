"""
Módulo para geração de relatórios em múltiplos formatos.
"""
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import json

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False


class GeradorRelatorios:
    """Classe para geração de relatórios em múltiplos formatos."""
    
    def __init__(self, output_dir: str = "data/relatorios"):
        """
        Inicializa o gerador de relatórios.
        
        Args:
            output_dir: Diretório de saída para relatórios
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
    
    def gerar_relatorio_txt(self, pontos: List[Dict[str, Any]], estatisticas: Optional[Dict[str, Any]] = None) -> str:
        """
        Gera relatório em formato TXT.
        
        Args:
            pontos: Lista de pontos
            estatisticas: Estatísticas (opcional)
            
        Returns:
            Caminho do arquivo gerado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"relatorio_{timestamp}.txt"
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                # Cabeçalho
                f.write("=" * 70 + "\n")
                f.write("RELATÓRIO DE CONECTIVIDADE RURAL\n")
                f.write("=" * 70 + "\n\n")
                
                f.write(f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Total de pontos mapeados: {len(pontos)}\n\n")
                
                # Estatísticas
                if estatisticas:
                    f.write("-" * 70 + "\n")
                    f.write("ESTATÍSTICAS GERAIS\n")
                    f.write("-" * 70 + "\n")
                    
                    for key, value in estatisticas.items():
                        if isinstance(value, dict):
                            f.write(f"\n{key.replace('_', ' ').title()}:\n")
                            for subkey, subvalue in value.items():
                                if isinstance(subvalue, (int, float)):
                                    f.write(f"  {subkey}: {subvalue:.2f}\n")
                                else:
                                    f.write(f"  {subkey}: {subvalue}\n")
                        else:
                            if isinstance(value, (int, float)):
                                f.write(f"{key.replace('_', ' ').title()}: {value:.2f}\n")
                            else:
                                f.write(f"{key.replace('_', ' ').title()}: {value}\n")
                    f.write("\n")
                
                # Detalhes dos pontos
                f.write("-" * 70 + "\n")
                f.write("PONTOS DE ACESSO\n")
                f.write("-" * 70 + "\n\n")
                
                for i, ponto in enumerate(pontos, 1):
                    f.write(f"Ponto {i}: {ponto.get('id', 'N/A')}\n")
                    
                    if 'nome' in ponto:
                        f.write(f"  Nome: {ponto['nome']}\n")
                    
                    if 'comunidade' in ponto:
                        f.write(f"  Comunidade: {ponto['comunidade']}\n")
                    
                    if 'provedor' in ponto:
                        f.write(f"  Provedor: {ponto['provedor']}\n")
                    
                    if 'tecnologia' in ponto:
                        f.write(f"  Tecnologia: {ponto['tecnologia']}\n")
                    
                    if 'latitude' in ponto and 'longitude' in ponto:
                        f.write(f"  Localização: {ponto['latitude']}, {ponto['longitude']}\n")
                    elif 'x' in ponto and 'y' in ponto:
                        f.write(f"  Coordenadas: ({ponto['x']}, {ponto['y']})\n")
                    
                    if 'velocidade_download' in ponto:
                        f.write(f"  Velocidade Download: {ponto['velocidade_download']:.2f} Mbps\n")
                    
                    if 'velocidade_upload' in ponto:
                        f.write(f"  Velocidade Upload: {ponto['velocidade_upload']:.2f} Mbps\n")
                    
                    if 'latencia' in ponto:
                        f.write(f"  Latência: {ponto['latencia']:.2f} ms\n")
                    
                    if 'status' in ponto:
                        f.write(f"  Status: {ponto['status']}\n")
                    
                    if 'observacoes' in ponto and ponto['observacoes']:
                        f.write(f"  Observações: {ponto['observacoes']}\n")
                    
                    f.write("\n")
                
                f.write("=" * 70 + "\n")
                f.write("Fim do relatório\n")
                f.write("=" * 70 + "\n")
            
            return str(filepath)
        
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar relatório TXT: {e}")
    
    def gerar_relatorio_json(self, pontos: List[Dict[str, Any]], estatisticas: Optional[Dict[str, Any]] = None) -> str:
        """
        Gera relatório em formato JSON.
        
        Args:
            pontos: Lista de pontos
            estatisticas: Estatísticas (opcional)
            
        Returns:
            Caminho do arquivo gerado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"relatorio_{timestamp}.json"
        filepath = self.output_dir / filename
        
        try:
            relatorio = {
                'data_geracao': datetime.now().isoformat(),
                'total_pontos': len(pontos),
                'pontos': pontos
            }
            
            if estatisticas:
                relatorio['estatisticas'] = estatisticas
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(relatorio, f, indent=2, ensure_ascii=False, default=str)
            
            return str(filepath)
        
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar relatório JSON: {e}")
    
    def gerar_relatorio_csv(self, pontos: List[Dict[str, Any]], estatisticas: Optional[Dict[str, Any]] = None) -> str:
        """
        Gera relatório em formato CSV.
        
        Args:
            pontos: Lista de pontos
            estatisticas: Estatísticas (opcional, não incluídas no CSV)
            
        Returns:
            Caminho do arquivo gerado
        """
        if not PANDAS_AVAILABLE:
            raise RuntimeError("Pandas não está instalado. Instale com: pip install pandas")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"relatorio_{timestamp}.csv"
        filepath = self.output_dir / filename
        
        try:
            df = pd.DataFrame(pontos)
            df.to_csv(filepath, index=False, encoding='utf-8')
            
            return str(filepath)
        
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar relatório CSV: {e}")
    
    def gerar_relatorio_html(self, pontos: List[Dict[str, Any]], estatisticas: Optional[Dict[str, Any]] = None) -> str:
        """
        Gera relatório em formato HTML.
        
        Args:
            pontos: Lista de pontos
            estatisticas: Estatísticas (opcional)
            
        Returns:
            Caminho do arquivo gerado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"relatorio_{timestamp}.html"
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("<!DOCTYPE html>\n")
                f.write("<html lang='pt-BR'>\n")
                f.write("<head>\n")
                f.write("    <meta charset='UTF-8'>\n")
                f.write("    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
                f.write("    <title>Relatório de Conectividade Rural</title>\n")
                f.write("    <style>\n")
                f.write("        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }\n")
                f.write("        .container { max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }\n")
                f.write("        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }\n")
                f.write("        h2 { color: #34495e; margin-top: 30px; }\n")
                f.write("        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }\n")
                f.write("        .stat-card { background-color: #ecf0f1; padding: 15px; border-radius: 5px; }\n")
                f.write("        .stat-card h3 { margin: 0 0 10px 0; color: #2c3e50; }\n")
                f.write("        table { width: 100%; border-collapse: collapse; margin: 20px 0; }\n")
                f.write("        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }\n")
                f.write("        th { background-color: #3498db; color: white; }\n")
                f.write("        tr:hover { background-color: #f5f5f5; }\n")
                f.write("        .footer { margin-top: 30px; text-align: center; color: #7f8c8d; font-size: 0.9em; }\n")
                f.write("    </style>\n")
                f.write("</head>\n")
                f.write("<body>\n")
                f.write("    <div class='container'>\n")
                f.write("        <h1>Relatório de Conectividade Rural</h1>\n")
                f.write(f"        <p><strong>Data de geração:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>\n")
                f.write(f"        <p><strong>Total de pontos mapeados:</strong> {len(pontos)}</p>\n")
                
                # Estatísticas
                if estatisticas:
                    f.write("        <h2>Estatísticas Gerais</h2>\n")
                    f.write("        <div class='stats'>\n")
                    
                    for key, value in estatisticas.items():
                        if isinstance(value, dict):
                            f.write("            <div class='stat-card'>\n")
                            f.write(f"                <h3>{key.replace('_', ' ').title()}</h3>\n")
                            for subkey, subvalue in value.items():
                                if isinstance(subvalue, float):
                                    f.write(f"                <p><strong>{subkey}:</strong> {subvalue:.2f}</p>\n")
                                else:
                                    f.write(f"                <p><strong>{subkey}:</strong> {subvalue}</p>\n")
                            f.write("            </div>\n")
                    
                    f.write("        </div>\n")
                
                # Tabela de pontos
                f.write("        <h2>Pontos de Acesso</h2>\n")
                f.write("        <table>\n")
                f.write("            <thead>\n")
                f.write("                <tr>\n")
                f.write("                    <th>ID</th>\n")
                f.write("                    <th>Nome</th>\n")
                f.write("                    <th>Comunidade</th>\n")
                f.write("                    <th>Provedor</th>\n")
                f.write("                    <th>Tecnologia</th>\n")
                f.write("                    <th>Download (Mbps)</th>\n")
                f.write("                    <th>Upload (Mbps)</th>\n")
                f.write("                    <th>Latência (ms)</th>\n")
                f.write("                    <th>Status</th>\n")
                f.write("                </tr>\n")
                f.write("            </thead>\n")
                f.write("            <tbody>\n")
                
                for ponto in pontos:
                    f.write("                <tr>\n")
                    f.write(f"                    <td>{ponto.get('id', 'N/A')}</td>\n")
                    f.write(f"                    <td>{ponto.get('nome', 'N/A')}</td>\n")
                    f.write(f"                    <td>{ponto.get('comunidade', 'N/A')}</td>\n")
                    f.write(f"                    <td>{ponto.get('provedor', 'N/A')}</td>\n")
                    f.write(f"                    <td>{ponto.get('tecnologia', 'N/A')}</td>\n")
                    
                    vel_down = ponto.get('velocidade_download')
                    vel_down_str = f"{vel_down:.2f}" if vel_down is not None else "N/A"
                    f.write(f"                    <td>{vel_down_str}</td>\n")
                    
                    vel_up = ponto.get('velocidade_upload')
                    vel_up_str = f"{vel_up:.2f}" if vel_up is not None else "N/A"
                    f.write(f"                    <td>{vel_up_str}</td>\n")
                    
                    lat = ponto.get('latencia')
                    lat_str = f"{lat:.2f}" if lat is not None else "N/A"
                    f.write(f"                    <td>{lat_str}</td>\n")
                    
                    f.write(f"                    <td>{ponto.get('status', 'N/A')}</td>\n")
                    f.write("                </tr>\n")
                
                f.write("            </tbody>\n")
                f.write("        </table>\n")
                
                f.write("        <div class='footer'>\n")
                f.write("            <p>Relatório gerado pelo Mapeador de Conectividade Rural</p>\n")
                f.write("        </div>\n")
                f.write("    </div>\n")
                f.write("</body>\n")
                f.write("</html>\n")
            
            return str(filepath)
        
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar relatório HTML: {e}")
    
    def gerar_relatorio_completo(self, pontos: List[Dict[str, Any]], estatisticas: Optional[Dict[str, Any]] = None, 
                                 formatos: Optional[List[str]] = None) -> Dict[str, str]:
        """
        Gera relatórios em múltiplos formatos.
        
        Args:
            pontos: Lista de pontos
            estatisticas: Estatísticas (opcional)
            formatos: Lista de formatos desejados ('txt', 'json', 'csv', 'html'). 
                     Se None, gera ['txt', 'json']
            
        Returns:
            Dicionário com formato como chave e caminho do arquivo como valor
        """
        if formatos is None:
            formatos = ['txt', 'json']
        
        relatorios = {}
        erros = []
        
        for formato in formatos:
            formato = formato.lower()
            try:
                if formato == 'txt':
                    relatorios['txt'] = self.gerar_relatorio_txt(pontos, estatisticas)
                elif formato == 'json':
                    relatorios['json'] = self.gerar_relatorio_json(pontos, estatisticas)
                elif formato == 'csv':
                    relatorios['csv'] = self.gerar_relatorio_csv(pontos, estatisticas)
                elif formato == 'html':
                    relatorios['html'] = self.gerar_relatorio_html(pontos, estatisticas)
                else:
                    erros.append(f"Formato '{formato}' não suportado")
            except Exception as e:
                erros.append(f"Erro ao gerar relatório {formato}: {e}")
        
        if erros:
            # Log errors but continue if at least one format succeeded
            import sys
            for erro in erros:
                print(erro, file=sys.stderr)
        
        return relatorios

    def gerar_relatorio_personalizado(self, pontos: List[Dict[str, Any]], estatisticas: Optional[Dict[str, Any]] = None, 
                                      opcoes: Optional[List[str]] = None) -> str:
        """
        Gera relatório personalizado com opções selecionáveis.
        
        Args:
            pontos: Lista de pontos
            estatisticas: Estatísticas (opcional)
            opcoes: Lista de opções (1-6). Se None, modo interativo
            
        Returns:
            Caminho do arquivo gerado
        """
        # Importar colorama se disponível
        try:
            from colorama import Fore, Style, init as colorama_init
            colorama_init(autoreset=True)
        except ImportError:
            class Fore:
                RED = GREEN = YELLOW = BLUE = CYAN = MAGENTA = WHITE = RESET = ""
            class Style:
                BRIGHT = RESET_ALL = ""
        
        # Se opcoes não fornecidas, entrar em modo interativo
        if opcoes is None:
            print(f"\n{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}GERADOR DE RELATÓRIO PERSONALIZADO{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")
            
            print("Incluir no relatório:")
            print("1. ✅ Estatísticas gerais")
            print("2. ✅ Lista completa de pontos")
            print("3. ⚙️  Apenas pontos com medição")
            print("4. ⚙️  Apenas pontos críticos (< 10 Mbps)")
            print("5. ⚙️  Recomendações")
            print("6. ⚙️  Metodologia")
            
            entrada = input(f"\n{Fore.GREEN}Selecione opções (separadas por vírgula): {Style.RESET_ALL}").strip()
            opcoes = [o.strip() for o in entrada.split(',') if o.strip()]
        
        # Validar opcoes
        opcoes_validas = [o for o in opcoes if o in ['1', '2', '3', '4', '5', '6']]
        
        # Filtrar dados conforme opções
        dados_filtrados = pontos.copy()
        filtro_aplicado = None
        
        if "3" in opcoes_validas:
            dados_filtrados = [d for d in dados_filtrados if d.get('velocidade_download')]
            filtro_aplicado = "Apenas pontos com medição"
        
        if "4" in opcoes_validas:
            dados_filtrados = [d for d in dados_filtrados if d.get('velocidade_download', 100) < 10]
            filtro_aplicado = "Apenas pontos críticos (< 10 Mbps)"
        
        # Gerar relatório
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"relatorio_personalizado_{timestamp}.txt"
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                # Cabeçalho
                f.write("=" * 70 + "\n")
                f.write("RELATÓRIO PERSONALIZADO - MAPEADOR DE CONECTIVIDADE RURAL\n")
                f.write("=" * 70 + "\n\n")
                
                f.write(f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Total de pontos analisados: {len(pontos)}\n")
                if filtro_aplicado:
                    f.write(f"Filtro aplicado: {filtro_aplicado}\n")
                f.write(f"Pontos no relatório: {len(dados_filtrados)}\n\n")
                
                # Estatísticas gerais
                if "1" in opcoes_validas and estatisticas:
                    f.write("-" * 70 + "\n")
                    f.write("ESTATÍSTICAS GERAIS\n")
                    f.write("-" * 70 + "\n\n")
                    
                    for key, value in estatisticas.items():
                        if isinstance(value, dict):
                            f.write(f"{key.replace('_', ' ').title()}:\n")
                            for subkey, subvalue in value.items():
                                if isinstance(subvalue, (int, float)):
                                    f.write(f"  • {subkey}: {subvalue:.2f}\n")
                                else:
                                    f.write(f"  • {subkey}: {subvalue}\n")
                            f.write("\n")
                        else:
                            if isinstance(value, (int, float)):
                                f.write(f"{key.replace('_', ' ').title()}: {value:.2f}\n")
                            else:
                                f.write(f"{key.replace('_', ' ').title()}: {value}\n")
                    f.write("\n")
                
                # Lista de pontos
                if ("2" in opcoes_validas or "3" in opcoes_validas or "4" in opcoes_validas) and dados_filtrados:
                    f.write("-" * 70 + "\n")
                    f.write(f"PONTOS DE ACESSO ({len(dados_filtrados)})\n")
                    f.write("-" * 70 + "\n\n")
                    
                    for i, ponto in enumerate(dados_filtrados, 1):
                        f.write(f"Ponto {i}: {ponto.get('id', 'N/A')}\n")
                        
                        if 'nome' in ponto:
                            f.write(f"  • Nome: {ponto['nome']}\n")
                        
                        if 'comunidade' in ponto:
                            f.write(f"  • Comunidade: {ponto['comunidade']}\n")
                        
                        if 'provedor' in ponto:
                            f.write(f"  • Provedor: {ponto['provedor']}\n")
                        
                        if 'tecnologia' in ponto:
                            f.write(f"  • Tecnologia: {ponto['tecnologia']}\n")
                        
                        if 'velocidade_download' in ponto:
                            vel = ponto['velocidade_download']
                            status_velocidade = "🔴 CRÍTICO" if vel < 10 else "🟡 BAIXO" if vel < 25 else "🟢 ADEQUADO"
                            f.write(f"  • Velocidade Download: {vel:.2f} Mbps {status_velocidade}\n")
                        
                        if 'velocidade_upload' in ponto:
                            f.write(f"  • Velocidade Upload: {ponto['velocidade_upload']:.2f} Mbps\n")
                        
                        if 'latencia' in ponto:
                            lat = ponto['latencia']
                            status_lat = "🔴 ALTA" if lat > 100 else "🟡 MODERADA" if lat > 50 else "🟢 BAIXA"
                            f.write(f"  • Latência: {lat:.2f} ms {status_lat}\n")
                        
                        if 'status' in ponto:
                            f.write(f"  • Status: {ponto['status']}\n")
                        
                        f.write("\n")
                
                # Recomendações
                if "5" in opcoes_validas:
                    f.write("-" * 70 + "\n")
                    f.write("RECOMENDAÇÕES\n")
                    f.write("-" * 70 + "\n\n")
                    
                    # Analisar pontos críticos
                    pontos_criticos = [p for p in pontos if p.get('velocidade_download', 100) < 10]
                    pontos_inativos = [p for p in pontos if p.get('status', 'ativo') != 'ativo']
                    
                    if pontos_criticos:
                        f.write(f"⚠️  URGENTE: {len(pontos_criticos)} ponto(s) com velocidade crítica (< 10 Mbps)\n")
                        f.write("   Recomendação: Avaliar upgrade de tecnologia ou substituição de provedor\n\n")
                    
                    if pontos_inativos:
                        f.write(f"⚠️  ATENÇÃO: {len(pontos_inativos)} ponto(s) inativo(s)\n")
                        f.write("   Recomendação: Verificar manutenção e reativar serviços\n\n")
                    
                    # Análise de cobertura por tecnologia
                    tecnologias = {}
                    for p in pontos:
                        tech = p.get('tecnologia', 'Desconhecida')
                        tecnologias[tech] = tecnologias.get(tech, 0) + 1
                    
                    f.write("📊 Distribuição de Tecnologias:\n")
                    for tech, count in sorted(tecnologias.items(), key=lambda x: x[1], reverse=True):
                        f.write(f"   • {tech}: {count} ponto(s)\n")
                    f.write("\n")
                    
                    # Recomendações gerais
                    f.write("📋 Recomendações Gerais:\n")
                    f.write("   1. Priorizar áreas com velocidade < 25 Mbps para expansão\n")
                    f.write("   2. Considerar tecnologias satelitais (Starlink) para áreas remotas\n")
                    f.write("   3. Implementar monitoramento contínuo de qualidade\n")
                    f.write("   4. Estabelecer SLA mínimo de 25 Mbps para inclusão digital\n\n")
                
                # Metodologia
                if "6" in opcoes_validas:
                    f.write("-" * 70 + "\n")
                    f.write("METODOLOGIA\n")
                    f.write("-" * 70 + "\n\n")
                    
                    f.write("📖 Processo de Coleta de Dados:\n\n")
                    f.write("1. LEVANTAMENTO:\n")
                    f.write("   • Identificação de pontos de acesso existentes\n")
                    f.write("   • Coleta de coordenadas GPS\n")
                    f.write("   • Registro de informações de provedor e tecnologia\n\n")
                    
                    f.write("2. MEDIÇÕES:\n")
                    f.write("   • Testes de velocidade (download/upload)\n")
                    f.write("   • Medição de latência\n")
                    f.write("   • Avaliação de estabilidade da conexão\n\n")
                    
                    f.write("3. ANÁLISE:\n")
                    f.write("   • Cálculo de estatísticas agregadas\n")
                    f.write("   • Identificação de pontos críticos\n")
                    f.write("   • Mapeamento de áreas de baixa cobertura\n\n")
                    
                    f.write("4. CLASSIFICAÇÃO:\n")
                    f.write("   • Adequado: ≥ 25 Mbps download\n")
                    f.write("   • Baixo: 10-25 Mbps download\n")
                    f.write("   • Crítico: < 10 Mbps download\n")
                    f.write("   • Latência Baixa: ≤ 50 ms\n")
                    f.write("   • Latência Moderada: 50-100 ms\n")
                    f.write("   • Latência Alta: > 100 ms\n\n")
                
                # Rodapé
                f.write("=" * 70 + "\n")
                f.write("Relatório gerado pelo Mapeador de Conectividade Rural\n")
                f.write("Para mais informações: https://github.com/danielnovais-tech\n")
                f.write("=" * 70 + "\n")
            
            if opcoes is None:  # Modo interativo
                print(f"\n{Fore.GREEN}✅ Relatório personalizado gerado com sucesso!{Style.RESET_ALL}")
                print(f"📄 Arquivo: {filepath}\n")
            
            return str(filepath)
        
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar relatório personalizado: {e}")
