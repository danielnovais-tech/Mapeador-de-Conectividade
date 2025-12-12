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
                                if isinstance(subvalue, float):
                                    f.write(f"  {subkey}: {subvalue:.2f}\n")
                                else:
                                    f.write(f"  {subkey}: {subvalue}\n")
                        else:
                            if isinstance(value, float):
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
    
    def gerar_relatorio_csv(self, pontos: List[Dict[str, Any]]) -> str:
        """
        Gera relatório em formato CSV.
        
        Args:
            pontos: Lista de pontos
            
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
                                 formatos: List[str] = ['txt', 'json']) -> Dict[str, str]:
        """
        Gera relatórios em múltiplos formatos.
        
        Args:
            pontos: Lista de pontos
            estatisticas: Estatísticas (opcional)
            formatos: Lista de formatos desejados ('txt', 'json', 'csv', 'html')
            
        Returns:
            Dicionário com formato como chave e caminho do arquivo como valor
        """
        relatorios = {}
        
        for formato in formatos:
            formato = formato.lower()
            try:
                if formato == 'txt':
                    relatorios['txt'] = self.gerar_relatorio_txt(pontos, estatisticas)
                elif formato == 'json':
                    relatorios['json'] = self.gerar_relatorio_json(pontos, estatisticas)
                elif formato == 'csv':
                    relatorios['csv'] = self.gerar_relatorio_csv(pontos)
                elif formato == 'html':
                    relatorios['html'] = self.gerar_relatorio_html(pontos, estatisticas)
                else:
                    print(f"Aviso: Formato '{formato}' não suportado")
            except Exception as e:
                print(f"Erro ao gerar relatório {formato}: {e}")
        
        return relatorios
